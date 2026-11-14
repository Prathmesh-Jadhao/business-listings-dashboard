
import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"

CITIES = ["Pune", "Mumbai"]

REQUIRED_COLUMNS = [
    "business_name",
    "category",
    "city",
    "address",
    "phone",
    "source",
]


def clean_text(value):
    """Trim whitespace and convert empty strings to missing values."""
    if isinstance(value, str):
        value = value.strip()
        return value if value else None
    return value


def clean_city_dataset(city):
    input_file = DATA_DIR / f"osm_{city.lower()}_listings.csv"
    output_file = DATA_DIR / f"osm_{city.lower()}_listings_cleaned.csv"

    if not input_file.exists():
        print(f"\n{city}: Input file not found. Skipping.")
        return

    print(f"\nCleaning {city} dataset...")

    df = pd.read_csv(input_file)

    original_count = len(df)

    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"{city}: Missing columns: {missing_columns}"
        )

    # Keep only the required fields in a consistent order.
    df = df[REQUIRED_COLUMNS].copy()

    # Clean whitespace in text fields.
    for column in REQUIRED_COLUMNS:
        df[column] = df[column].apply(clean_text)

    # The collector queried this specific city.
    # Standardize its city field consistently.
    df["city"] = city

    # Remove rows without a business/place name.
    df = df.dropna(subset=["business_name"])

    # Replace generic category values.
    df["category"] = df["category"].replace({
        "Yes": "Uncategorized",
        "yes": "Uncategorized",
    })

    df["category"] = df["category"].fillna("Uncategorized")

    # Remove duplicate records within this city.
    df = df.drop_duplicates(
        subset=["business_name", "address", "city"]
    )

    # Save cleaned dataset.
    df.to_csv(
        output_file,
        index=False,
        encoding="utf-8-sig"
    )

    print(f"Original records: {original_count}")
    print(f"Cleaned records: {len(df)}")
    print(f"Duplicates/invalid rows removed: {original_count - len(df)}")
    print(f"Missing addresses: {df['address'].isna().sum()}")
    print(f"Missing phone numbers: {df['phone'].isna().sum()}")
    print(f"Unique categories: {df['category'].nunique()}")
    print(f"Saved: {output_file}")


def main():
    print("Starting multi-city OSM data cleaning...")

    total_cleaned = 0

    for city in CITIES:
        clean_city_dataset(city)

        output_file = DATA_DIR / f"osm_{city.lower()}_listings_cleaned.csv"

        if output_file.exists():
            df = pd.read_csv(output_file)
            total_cleaned += len(df)

    print("\n" + "=" * 45)
    print("ALL CITY DATASETS CLEANED")
    print(f"Combined cleaned records: {total_cleaned}")
    print("=" * 45)


if __name__ == "__main__":
    main()
