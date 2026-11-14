
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import SessionLocal
from app.models import Listing

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/city-wise")
def city_wise_count(db: Session = Depends(get_db)):
    results = (
        db.query(
            Listing.city,
            func.count(Listing.id).label("total")
        )
        .group_by(Listing.city)
        .order_by(func.count(Listing.id).desc())
        .all()
    )

    return [
        {"city": city, "total": total}
        for city, total in results
    ]


@router.get("/category-wise")
def category_wise_count(db: Session = Depends(get_db)):
    results = (
        db.query(
            Listing.category,
            func.count(Listing.id).label("total")
        )
        .group_by(Listing.category)
        .order_by(func.count(Listing.id).desc())
        .all()
    )

    return [
        {"category": category, "total": total}
        for category, total in results
    ]


@router.get("/source-wise")
def source_wise_count(db: Session = Depends(get_db)):
    results = (
        db.query(
            Listing.source,
            func.count(Listing.id).label("total")
        )
        .group_by(Listing.source)
        .order_by(func.count(Listing.id).desc())
        .all()
    )

    return [
        {"source": source, "total": total}
        for source, total in results
    ]

@router.get("/summary")
def dashboard_summary(db: Session = Depends(get_db)):
    total = db.query(func.count(Listing.id)).scalar()

    return {
        "total_listings": total
    }