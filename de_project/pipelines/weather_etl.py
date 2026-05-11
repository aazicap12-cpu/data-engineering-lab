"""
PROJECT 1: Real-Time Weather ETL Pipeline
==========================================
Extracts weather data from OpenWeather API
Transforms and validates the data
Loads into PostgreSQL data warehouse

Interview talking point:
  "Built a production-style ETL pipeline with API ingestion,
   data validation, and PostgreSQL loading using Python and SQLAlchemy."
"""

import requests
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ── CONFIG ───────────────────────────────────────────────
DB_CONN = "postgresql://deuser:depass123@localhost:5432/de_lab"
API_KEY  = os.getenv("OPENWEATHER_API_KEY", "demo_key")  # set in .env file

CITIES = [
    {"name": "Mumbai",    "lat": 19.0760, "lon": 72.8777},
    {"name": "Bangalore", "lat": 12.9716, "lon": 77.5946},
    {"name": "Kochi",     "lat": 9.9312,  "lon": 76.2673},
    {"name": "Delhi",     "lat": 28.6139, "lon": 77.2090},
    {"name": "Chennai",   "lat": 13.0827, "lon": 80.2707},
]

# ── EXTRACT ──────────────────────────────────────────────
def extract_weather(city: dict) -> dict | None:
    """Fetch weather data from OpenWeather API."""
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat":   city["lat"],
        "lon":   city["lon"],
        "appid": API_KEY,
        "units": "metric"
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        logger.info(f"✅ Extracted: {city['name']}")
        return response.json()
    except requests.RequestException as e:
        logger.error(f"❌ Failed {city['name']}: {e}")
        return None

# ── TRANSFORM ────────────────────────────────────────────
def transform_weather(raw: dict, city_name: str) -> dict:
    """Clean and structure raw API response."""
    return {
        "city":            city_name,
        "country":         raw.get("sys", {}).get("country", "IN"),
        "temperature_c":   round(raw["main"]["temp"], 2),
        "feels_like_c":    round(raw["main"]["feels_like"], 2),
        "humidity_pct":    raw["main"]["humidity"],
        "pressure_hpa":    raw["main"]["pressure"],
        "wind_speed_ms":   raw.get("wind", {}).get("speed", 0),
        "weather_desc":    raw["weather"][0]["description"],
        "weather_main":    raw["weather"][0]["main"],
        "visibility_m":    raw.get("visibility", None),
        "cloudiness_pct":  raw.get("clouds", {}).get("all", 0),
        "ingested_at":     datetime.utcnow(),
        "source":          "openweather_api"
    }

# ── VALIDATE ─────────────────────────────────────────────
def validate(record: dict) -> bool:
    """Data quality checks — a real DE practice."""
    checks = [
        record["temperature_c"] > -50,
        record["temperature_c"] < 60,
        0 <= record["humidity_pct"] <= 100,
        record["city"] is not None,
    ]
    return all(checks)

# ── LOAD ─────────────────────────────────────────────────
def create_table(engine):
    """Create warehouse table if not exists."""
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS weather_raw (
                id              SERIAL PRIMARY KEY,
                city            VARCHAR(100),
                country         VARCHAR(10),
                temperature_c   NUMERIC(5,2),
                feels_like_c    NUMERIC(5,2),
                humidity_pct    INTEGER,
                pressure_hpa    INTEGER,
                wind_speed_ms   NUMERIC(6,2),
                weather_desc    VARCHAR(200),
                weather_main    VARCHAR(100),
                visibility_m    INTEGER,
                cloudiness_pct  INTEGER,
                ingested_at     TIMESTAMP,
                source          VARCHAR(50)
            );
        """))
        conn.commit()
    logger.info("✅ Table weather_raw ready")

def load(records: list[dict], engine):
    """Load transformed records to PostgreSQL."""
    df = pd.DataFrame(records)
    df.to_sql("weather_raw", engine, if_exists="append", index=False)
    logger.info(f"✅ Loaded {len(records)} records to PostgreSQL")

# ── PIPELINE ORCHESTRATION ───────────────────────────────
def run_pipeline():
    logger.info("🚀 Starting Weather ETL Pipeline")
    engine = create_engine(DB_CONN)
    create_table(engine)

    records = []
    for city in CITIES:
        raw = extract_weather(city)
        if raw:
            record = transform_weather(raw, city["name"])
            if validate(record):
                records.append(record)
                logger.info(f"✅ Validated: {city['name']} — {record['temperature_c']}°C")
            else:
                logger.warning(f"⚠️ Validation failed: {city['name']}")

    if records:
        load(records, engine)
        logger.info(f"🎉 Pipeline complete — {len(records)}/{len(CITIES)} cities loaded")
    else:
        logger.error("❌ No records to load")

if __name__ == "__main__":
    run_pipeline()
