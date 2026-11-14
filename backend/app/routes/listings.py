
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Listing
from app.schemas import (
    BulkListingCreate,
    BulkListingResponse,
    ListingPageResponse,
)

router = APIRouter(prefix="/api/listings", tags=["Listings"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Existing bulk insert API
@router.post("/bulk", response_model=BulkListingResponse)
def bulk_insert_listings(
    payload: BulkListingCreate,
    db: Session = Depends(get_db)
):
    try:
        listings = [
            Listing(**listing.model_dump())
            for listing in payload.listings
        ]

        db.add_all(listings)
        db.commit()

        return BulkListingResponse(
            message="Listings inserted successfully",
            inserted_count=len(listings),
            listing_ids=[listing.id for listing in listings]
        )

    except Exception as error:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to insert listings: {str(error)}"
        )


# New search, filter and pagination API
@router.get("", response_model=ListingPageResponse)
def get_listings(
    search: str | None = Query(default=None),
    city: str | None = Query(default=None),
    category: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    try:
        query = db.query(Listing)

        # Search business names
        if search and search.strip():
            query = query.filter(
                Listing.business_name.ilike(f"%{search.strip()}%")
            )

        # Filter by city
        if city and city.strip():
            query = query.filter(
                Listing.city.ilike(city.strip())
            )

        # Filter by category
        if category and category.strip():
            query = query.filter(
                Listing.category.ilike(category.strip())
            )

        # Count matching records before pagination
        total = query.count()

        # Calculate pagination
        total_pages = (total + page_size - 1) // page_size

        # Fetch only the requested page
        listings = (
            query
            .order_by(Listing.business_name.asc(), Listing.id.asc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        return ListingPageResponse(
            items=listings,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch listings: {str(error)}"
        )
