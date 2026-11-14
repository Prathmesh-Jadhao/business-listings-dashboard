# Business Listings Dashboard

A full-stack business listings analytics dashboard built using **React, FastAPI, and MySQL**. It collects business and place listings from OpenStreetMap for Pune and Mumbai, stores the data in MySQL, and provides an interface to explore listings and view analytics.

## Project Overview

The project brings together data collection, cleaning, database storage, API development, and frontend visualization in one application.

Users can view listing statistics, compare cities and categories, and search or filter individual records through the dashboard.

### Current Dataset

| Metric          |  Value |
| --------------- | -----: |
| Total listings  | 20,363 |
| Cities covered  |      2 |
| Pune listings   | 11,152 |
| Mumbai listings |  9,211 |
| Categories      |    427 |
| Data sources    |      1 |

**Data source:** OpenStreetMap

These figures represent the current collected dataset. Counts may change when the source data is updated and the collection process is run again.

## Features

- Collect named business and place listings from OpenStreetMap using the Overpass API.
- Save collected data as city-wise CSV files.
- Clean records and handle missing or inconsistent values.
- Remove duplicate records based on business name, address, and city.
- Store the cleaned records in MySQL.
- Provide REST APIs using FastAPI.
- Display total listing, city, category, and source statistics.
- Visualize city-wise and category-wise listing distributions.
- Search listings by business name.
- Filter listings by city and category.
- Explore records using pagination.
- Refresh dashboard statistics.

## Technology Stack

| Component       | Technology                           |
| --------------- | ------------------------------------ |
| Frontend        | React, Vite, JavaScript              |
| Charts          | Recharts                             |
| Icons           | Lucide React                         |
| HTTP Client     | Axios                                |
| Backend         | Python, FastAPI                      |
| Database        | MySQL                                |
| ORM             | SQLAlchemy                           |
| Data Processing | Pandas                               |
| Data Collection | Requests, OpenStreetMap Overpass API |

## Project Structure

```text
business-listings-dashboard/
│
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── main.py
│   │
│   └── scraper/
│       ├── collect_osm.py
│       ├── clean_osm.py
│       └── import_to_mysql.py
│
├── data/
│   ├── osm_pune_listings.csv
│   ├── osm_pune_listings_cleaned.csv
│   ├── osm_mumbai_listings.csv
│   └── osm_mumbai_listings_cleaned.csv
│
├── database/
│   └── business_listings_db.sql
│
└── frontend/
    ├── src/
    ├── package.json
    └── vite.config.js
```

## Database

**Database name:** `business_listings_db`

**Main table:** `listing_master`

The table contains the following fields:

| Column          | Description                   |
| --------------- | ----------------------------- |
| `id`            | Auto-incremented record ID    |
| `business_name` | Name of the business or place |
| `category`      | Listing category              |
| `city`          | City name                     |
| `address`       | Available address information |
| `phone`         | Available contact number      |
| `source`        | Data source                   |
| `created_at`    | Record creation timestamp     |

Phone numbers and addresses can be empty when that information is not available in the source data.

## Backend API

The backend is built with FastAPI and exposes the following endpoints:

| Method | Endpoint                       | Purpose                               |
| ------ | ------------------------------ | ------------------------------------- |
| GET    | `/health`                      | Backend health check                  |
| POST   | `/api/listings/bulk`           | Insert multiple listings              |
| GET    | `/api/listings`                | Search, filter, and paginate listings |
| GET    | `/api/dashboard/summary`       | Dashboard summary statistics          |
| GET    | `/api/dashboard/city-wise`     | City-wise listing counts              |
| GET    | `/api/dashboard/category-wise` | Category-wise listing counts          |
| GET    | `/api/dashboard/source-wise`   | Source-wise listing counts            |

The listing endpoint supports business-name search, city and category filters, and pagination.

FastAPI's interactive API documentation is available at:

`http://127.0.0.1:8000/docs`

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd business-listings-dashboard
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with the actual repository URL.

### 2. Set up the MySQL database

Create the database:

```sql
CREATE DATABASE business_listings_db;
```

If the repository includes the SQL dump, import it using:

```bash
mysql -u root -p business_listings_db < database/business_listings_db.sql
```

### 3. Set up the backend

From the project root, open a terminal and run:

```bash
cd backend
python -m venv .venv
```

Activate the virtual environment on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install the required packages:

```bash
pip install fastapi "uvicorn[standard]" sqlalchemy pymysql pydantic-settings pandas python-dotenv requests
```

Create a `.env` file inside the `backend` directory and configure the database connection variables expected by the backend configuration.

Start the backend server:

```bash
uvicorn app.main:app --reload
```

The backend should now be available at:

`http://127.0.0.1:8000`

### 4. Set up the frontend

Open a second terminal and navigate to the frontend directory:

```bash
cd frontend
npm install
npm run dev
```

Open the application in your browser:

`http://localhost:5173`

## Data Collection Pipeline

The project uses OpenStreetMap data through the Overpass API.

The collection and import process is divided into three scripts:

**1. Collection — `collect_osm.py`**

Collects named business and place listings for Pune and Mumbai and saves them into separate raw CSV files.

**2. Cleaning — `clean_osm.py`**

Processes the collected CSV files by trimming whitespace, standardizing city values, handling missing categories, and removing duplicate records.

**3. Database import — `import_to_mysql.py`**

Reads the cleaned CSV files and inserts records into the MySQL `listing_master` table. Before inserting, it checks existing business-name, address, and city combinations to avoid importing matching records again.

Run the scripts from the project root:

```bash
python backend/scraper/collect_osm.py
python backend/scraper/clean_osm.py
python backend/scraper/import_to_mysql.py
```

The collection script skips raw CSV files that already exist. To collect fresh data, handle the existing raw files intentionally before running the collection script again.

## Data Attribution

The data used in this project comes from **OpenStreetMap contributors**.

OpenStreetMap data is available under the Open Database License (ODbL). Please refer to the official attribution and licensing information:

[https://www.openstreetmap.org/copyright](https://www.openstreetmap.org/copyright)

## Limitations

- The number of listings depends on the data available in OpenStreetMap.
- Some records do not contain address or phone information.
- The dataset contains both commercial businesses and other named places or facilities.
- The accuracy and completeness of listings depend on the source data.
- The current collection covers Pune and Mumbai.
- Duplicate detection is based on business name, address, and city combinations.

## Future Improvements

- Extend data collection to additional cities.
- Add more data sources where collection and reuse are authorized.
- Improve duplicate detection and data validation.
- Add date-based analytics.
- Introduce CSV export functionality.
- Schedule automated data collection.
- Add more advanced filtering and reporting.

## License

The project code does not currently specify a separate open-source license.

OpenStreetMap data is subject to the Open Database License (ODbL). Refer to the official OpenStreetMap copyright page for attribution and licensing requirements.