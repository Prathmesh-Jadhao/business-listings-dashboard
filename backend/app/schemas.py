
from pydantic import BaseModel, ConfigDict, Field


class ListingCreate(BaseModel):
    business_name: str = Field(min_length=1, max_length=255)
    category: str | None = Field(default=None, max_length=100)
    city: str = Field(min_length=1, max_length=100)
    address: str | None = None
    phone: str | None = Field(default=None, max_length=255)
    source: str = Field(min_length=1, max_length=100)


class BulkListingCreate(BaseModel):
    listings: list[ListingCreate] = Field(min_length=1)


class ListingResponse(ListingCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class BulkListingResponse(BaseModel):
    message: str
    inserted_count: int
    listing_ids: list[int]

class ListingPageResponse(BaseModel):
    items: list[ListingResponse]
    total: int
    page: int
    page_size: int
    total_pages: int