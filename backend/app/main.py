from fastapi import FastAPI
from sqlalchemy import text

from app.database import engine
from app.database import SessionLocal
from app.models import Listing

from app.routes.listings import router as listings_router
from app.routes.dashboard import router as dashboard_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Business Listings Dashboard API",
    description="API for collecting and analyzing business listings",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://business-listings-dashboard-three.vercel.app",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(listings_router)
app.include_router(dashboard_router)


@app.get("/")
def home():
    return {
        "message": "Business Listings Dashboard API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/health/db")
def database_health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "connected",
            "database": "business_listings_db"
        }

    except Exception as error:
        return {
            "status": "error",
            "details": str(error)
        }

@app.get("/health/table")
def check_listing_table():
    db = SessionLocal()

    try:
        total = db.query(Listing).count()

        return {
            "status": "connected",
            "table": "listing_master",
            "total_records": total
        }

    except Exception as error:
        return {
            "status": "error",
            "details": str(error)
        }

    finally:
        db.close()