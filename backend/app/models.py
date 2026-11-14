
from sqlalchemy import Column, BigInteger, String, Text, DateTime
from sqlalchemy.sql import func

from app.database import Base


class Listing(Base):
    __tablename__ = "listing_master"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    business_name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=True)
    city = Column(String(100), nullable=False)
    address = Column(Text, nullable=True)
    phone = Column(String(255), nullable=True)
    source = Column(String(100), nullable=False)

    created_at = Column(
        DateTime,
        server_default=func.current_timestamp()
    )
