"""
AIRFLOW DAG — Weather ETL Pipeline
====================================
Schedules the weather ETL to run every 6 hours.

Interview talking point:
  "Orchestrated ETL pipeline with Apache Airflow DAGs,
   including task dependencies, retries, and failure alerts."
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta
import sys
import os

sys.path.append('/workspaces/de-lab')
from pipelines.weather_etl import run_pipeline, extract_weather, transform_weather, validate, load
from sqlalchemy import create_engine
import logging

logger = logging.getLogger(__name__)

DB_CONN = "postgresql://deuser:depass123@localhost:5432/de_lab"

CITIES = [
    {"name": "Mumbai",    "lat": 19.0760, "lon": 72.8777},
    {"name": "Kochi",     "lat": 9.9312,  "lon": 76.2673},
    {"name": "Bangalore", "lat": 12.9716, "lon": 77.5946},
    {"name": "Delhi",     "lat": 28.6139, "lon": 77.2090},
    {"name": "Chennai",   "lat": 13.0827, "lon": 80.2707},
]

# ── DEFAULT ARGS ─────────────────────────────────────────
default_args = {
    "owner":            "asif_t",
    "depends_on_past":  False,
    "start_date":       datetime(2024, 1, 1),
    "email_on_failure": False,
    "retries":          3,
    "retry_delay":      timedelta(minutes=5),
}

# ── TASK FUNCTIONS ───────────────────────────────────────
def task_extract(**context):
    """Extract raw data from API and push to XCom."""
    raw_data = []
    for city in CITIES:
        raw = extract_weather(city)
        if raw:
            raw_data.append({"city": city["name"], "raw": raw})
    context["ti"].xcom_push(key="raw_weather", value=raw_data)
    logger.info(f"Extracted {len(raw_data)} city records")

def task_transform(**context):
    """Transform raw data and push to XCom."""
    raw_data = context["ti"].xcom_pull(key="raw_weather", task_ids="extract")
    transformed = []
    for item in raw_data:
        record = transform_weather(item["raw"], item["city"])
        if validate(record):
            # Convert datetime for XCom serialisation
            record["ingested_at"] = record["ingested_at"].isoformat()
            transformed.append(record)
    context["ti"].xcom_push(key="transformed", value=transformed)
    logger.info(f"Transformed {len(transformed)} valid records")

def task_load(**context):
    """Load transformed data to PostgreSQL."""
    import pandas as pd
    from sqlalchemy import create_engine
    records = context["ti"].xcom_pull(key="transformed", task_ids="transform")
    df = pd.DataFrame(records)
    df["ingested_at"] = pd.to_datetime(df["ingested_at"])
    engine = create_engine(DB_CONN)
    df.to_sql("weather_raw", engine, if_exists="append", index=False)
    logger.info(f"Loaded {len(records)} records to PostgreSQL")

def task_quality_check(**context):
    """Run post-load data quality checks."""
    from sqlalchemy import create_engine, text
    engine = create_engine(DB_CONN)
    with engine.connect() as conn:
        result = conn.execute(text(
            "SELECT COUNT(*) FROM weather_raw WHERE ingested_at > NOW() - INTERVAL '1 hour'"
        )).fetchone()
        count = result[0]
        if count == 0:
            raise ValueError("❌ DQ Check failed: No fresh records in last 1 hour!")
        logger.info(f"✅ DQ Check passed: {count} fresh records found")

# ── DAG DEFINITION ───────────────────────────────────────
with DAG(
    dag_id="weather_etl_pipeline",
    default_args=default_args,
    description="Extract weather data every 6 hrs → PostgreSQL",
    schedule_interval="0 */6 * * *",  # every 6 hours
    catchup=False,
    tags=["etl", "weather", "postgresql", "data-engineering"],
) as dag:

    start = EmptyOperator(task_id="start")

    extract = PythonOperator(
        task_id="extract",
        python_callable=task_extract,
    )

    transform = PythonOperator(
        task_id="transform",
        python_callable=task_transform,
    )

    load_task = PythonOperator(
        task_id="load",
        python_callable=task_load,
    )

    quality_check = PythonOperator(
        task_id="quality_check",
        python_callable=task_quality_check,
    )

    end = EmptyOperator(task_id="end")

    # Task dependencies — DAG flow
    start >> extract >> transform >> load_task >> quality_check >> end
