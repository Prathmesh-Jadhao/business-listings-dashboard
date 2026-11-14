
import sys
import re
from pathlib import Path

import pandas as pd

BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

from app.database import SessionLocal
from app.models import Listing


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"

CITIES = ["Pune", "Mumbai"]
BATCH_SIZE = 1000

REQUIRED_COLUMNS = [
    "business_name",
    "category",
    "city",
    "address",
    "phone",
    "source",
]


def normalize(value):
    """Normalize values for duplicate comparison."""
    if value is None or pd.isna(value):
        return ""

    return re.sub(r"\s+", " ", str(value).strip().lower())


def make_key(name, address, city):
    return (
        normalize(name),
        normalize(address),
        normalize(city),
    )


def import_listings():
    db = SessionLocal()

    try:
        # Load existing database keys to prevent duplicate imports.
        existing_rows = db.query(
            Listing.business_name,
            Listing.address,
            Listing.city
        ).all()

        existing_keys = {
            make_key(name, address, city)
            for name, address, city in existing_rows
        }

        print(f"Existing database records: {len(existing_rows)}")

        total_inserted = 0
        total_skipped = 0

        for city in CITIES:
            csv_file = (
                DATA_DIR /
                f"osm_{city.lower()}_listings_cleaned.csv"
            )

            if not csv_file.exists():
                print(f"\n{city}: Cleaned CSV not found. Skipping.")
                continue

            print(f"\nImporting {city}...")

            df = pd.read_csv(csv_file)

            missing_columns = [
                col for col in REQUIRED_COLUMNS
                if col not in df.columns
            ]

            if missing_columns:
                raise ValueError(
                    f"{city}: Missing columns: {missing_columns}"
                )

            df = df[REQUIRED_COLUMNS]
            df = df.astype(object).where(pd.notna(df), None)

            records = df.to_dict(orient="records")

            city_inserted = 0
            city_skipped = 0
            batch = []

            for record in records:
                record["city"] = city

                key = make_key(
                    record["business_name"],
                    record["address"],
                    record["city"],
                )

                if not key[0]:
                    city_skipped += 1
                    continue

                if key in existing_keys:
                    city_skipped += 1
                    continue

                existing_keys.add(key)
                batch.append(record)

                if len(batch) >= BATCH_SIZE:
                    db.bulk_insert_mappings(Listing, batch)
                    db.commit()

                    city_inserted += len(batch)
                    print(
                        f"{city}: Inserted {city_inserted}/"
                        f"{len(records)} records"
                    )

                    batch = []

            # Insert remaining records.
            if batch:
                db.bulk_insert_mappings(Listing, batch)
                db.commit()
                city_inserted += len(batch)

            total_inserted += city_inserted
            total_skipped += city_skipped

            print(f"{city}: Import completed.")
            print(f"Inserted: {city_inserted}")
            print(f"Skipped: {city_skipped}")

        print("\n" + "=" * 45)
        print("IMPORT COMPLETED")
        print(f"New records inserted: {total_inserted}")
        print(f"Duplicate/invalid records skipped: {total_skipped}")
        print(f"Total records in MySQL: {db.query(Listing).count()}")
        print("=" * 45)

    except Exception as error:
        db.rollback()
        print(f"Import failed: {error}")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    import_listings()
