# 🚀 Data Engineering Lab — Modern ETL Pipeline

Production-style end-to-end Data Engineering project built using Python, PostgreSQL, dbt, Docker, Jupyter Notebook, and GitHub Codespaces.

---

# 🏗️ Architecture

```text
OpenWeather API
        ↓
Python ETL Pipeline
        ↓
Data Validation & Transformation
        ↓
PostgreSQL Data Warehouse
        ↓
dbt Staging Models
        ↓
dbt Mart Models
        ↓
Jupyter Notebook Analytics
```

---

# ⚡ Features

- Real-time weather API ingestion
- Python ETL pipeline
- Data validation checks
- PostgreSQL warehouse loading
- dbt layered transformations
- Staging → marts architecture
- Analytics-ready datasets
- Jupyter Notebook visualisation
- Cloud-based development using GitHub Codespaces

---

# 🛠️ Tech Stack

| Tool | Purpose |
|------|----------|
| Python | ETL scripting |
| PostgreSQL | Data warehouse |
| dbt | SQL transformations |
| Docker | PostgreSQL container |
| Pandas | Data processing |
| SQLAlchemy | Database connection |
| Jupyter Notebook | Analysis & visualisation |
| GitHub Codespaces | Cloud development environment |

---

# 📁 Project Structure

```text
data-engineering-lab/
│
├── de_project/
│   ├── dags/
│   │   └── weather_etl_dag.py
│   │
│   ├── dbt_project/
│   │   ├── dbt_project.yml
│   │   └── models/
│   │       ├── staging/
│   │       │   └── stg_weather.sql
│   │       │
│   │       └── marts/
│   │           └── mart_city_weather_summary.sql
│   │
│   ├── notebooks/
│   │   └── weather_analysis.ipynb
│   │
│   └── pipelines/
│       └── weather_etl.py
│
└── README.md
```

---

# ⚙️ Setup Instructions

## 1️⃣ Clone Repository

```bash
git clone <your-repo-url>
cd data-engineering-lab
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install requests pandas sqlalchemy psycopg2-binary matplotlib seaborn dbt-core dbt-postgres
```

---

## 4️⃣ Start PostgreSQL Using Docker

```bash
docker run --name postgres-weather \
-e POSTGRES_USER=deuser \
-e POSTGRES_PASSWORD=depass123 \
-e POSTGRES_DB=de_lab \
-p 5432:5432 \
-d postgres
```

---

## 5️⃣ Add OpenWeather API Key

```bash
export OPENWEATHER_API_KEY="your_api_key"
```

Free API:
https://openweathermap.org/api

---

## 6️⃣ Run ETL Pipeline

```bash
python de_project/pipelines/weather_etl.py
```

---

## 7️⃣ Run dbt Models

```bash
cd de_project/dbt_project
dbt run
```

---

# 📊 Example Analytics

The mart layer generates analytics-ready KPIs such as:

- Average city temperature
- Maximum & minimum temperature
- Average humidity
- Wind speed metrics
- Dominant weather condition
- Visibility metrics

---

# 🧠 Interview Talking Points

## ETL Pipeline

> Built a production-style ETL pipeline with API ingestion, transformation, validation, and PostgreSQL loading using Python.

---

## dbt Transformations

> Implemented modular SQL transformations using staging → marts layered architecture with dbt.

---

## Data Engineering Workflow

> Designed an end-to-end analytics workflow from raw API ingestion to business-ready reporting datasets.

---

## Cloud Development

> Developed and tested the entire project using GitHub Codespaces cloud environment.

---

# 📈 Future Improvements

- Apache Airflow orchestration
- Streamlit dashboard
- CI/CD using GitHub Actions
- Data quality testing with dbt tests
- AWS S3 integration
- DuckDB warehouse support

---

# 👨‍💻 Author

**Muhammed Asif T**

Aspiring Data Engineer focused on modern data stack technologies and cloud-based data pipelines.

---
