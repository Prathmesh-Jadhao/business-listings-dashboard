
import csv
import re
import time
import requests

from pathlib import Path


OVERPASS_URL = "https://overpass-api.de/api/interpreter"

CITIES = ["Pune", "Mumbai"]

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"


def normalize(value):
    return re.sub(r"\s+", " ", value.strip().lower())


def build_query(city):
    return f"""
    [out:json][timeout:180];

    area["name"="{city}"]["boundary"="administrative"]->.city_area;

    (
      nwr["name"]["shop"](area.city_area);
      nwr["name"]["amenity"](area.city_area);
      nwr["name"]["office"](area.city_area);
      nwr["name"]["craft"](area.city_area);
      nwr["name"]["healthcare"](area.city_area);
      nwr["name"]["tourism"](area.city_area);
    );

    out center tags;
    """


def extract_address(tags):
    if tags.get("addr:full"):
        return tags["addr:full"]

    parts = [
        tags.get("addr:housenumber"),
        tags.get("addr:street"),
        tags.get("addr:suburb"),
        tags.get("addr:neighbourhood"),
        tags.get("addr:postcode"),
    ]

    return ", ".join(part for part in parts if part)


def extract_category(tags):
    category_keys = [
        "shop",
        "amenity",
        "office",
        "craft",
        "healthcare",
        "tourism",
    ]

    for key in category_keys:
        if tags.get(key):
            return tags[key].replace("_", " ").title()

    return "Other"


def collect_city(city):
    output_file = DATA_DIR / f"osm_{city.lower()}_listings.csv"

    # Reuse existing Pune data instead of downloading it again.
    if output_file.exists():
        print(f"\n{city}: Existing CSV found. Skipping collection.")
        print(f"File: {output_file}")
        return

    print(f"\nCollecting {city} listings from OpenStreetMap...")

    headers = {
        "User-Agent": "BusinessListingsDashboard/1.0 (educational project)"
    }

    response = requests.post(
        OVERPASS_URL,
        data={"data": build_query(city)},
        headers=headers,
        timeout=240,
    )

    response.raise_for_status()

    elements = response.json().get("elements", [])

    print(f"{city}: Raw records received: {len(elements)}")

    listings = []
    seen = set()

    for element in elements:
        tags = element.get("tags", {})

        name = tags.get("name", "").strip()

        if not name:
            continue

        address = extract_address(tags)

        duplicate_key = (
            normalize(name),
            normalize(address),
            normalize(city),
        )

        if duplicate_key in seen:
            continue

        seen.add(duplicate_key)

        listings.append({
            "business_name": name,
            "category": extract_category(tags),
            "city": city,
            "address": address,
            "phone": (
                tags.get("contact:phone")
                or tags.get("phone")
                or None
            ),
            "source": "OpenStreetMap",
        })

    if not listings:
        print(f"{city}: No named listings found. No CSV created.")
        return

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with output_file.open(
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=listings[0].keys()
        )

        writer.writeheader()
        writer.writerows(listings)

    print(f"{city}: Saved {len(listings)} unique listings.")
    print(f"File: {output_file}")


def main():
    for index, city in enumerate(CITIES):
        try:
            collect_city(city)

        except requests.RequestException as error:
            print(f"{city}: Collection failed: {error}")

        except (ValueError, KeyError) as error:
            print(f"{city}: Could not process response: {error}")

        # Give the public Overpass service a break between requests.
        if index < len(CITIES) - 1:
            time.sleep(5)


if __name__ == "__main__":
    main()
