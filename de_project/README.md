# 🚀 Data Engineering Lab — GitHub Codespaces

**End-to-end Data Engineering project built for interview portfolio.**
Stack: Python · PostgreSQL · Apache Airflow · dbt · Jupyter · SQL

---

## 🏗️ Architecture

```
OpenWeather API
      ↓
Python ETL (extract → transform → validate)
      ↓
Apache Airflow (schedule every 6 hours)
      ↓
PostgreSQL (raw layer)
      ↓
dbt (staging → marts transformation)
      ↓
Jupyter Notebook (analysis & visualisation)
```

---

## ⚡ Quick Start — Codespaces

### Step 1 — Open in Codespaces
Click **Code → Codespaces → Create codespace on main**

Setup runs automatically (~5 min). All tools install by themselves.

### Step 2 — Add API Key
```bash
cp .env.example .env
# Edit .env and add your OpenWeather API key
# Free key at: openweathermap.org/api
```

### Step 3 — Run ETL Pipeline
```bash
python pipelines/weather_etl.py
```

### Step 4 — Start Airflow
```bash
export AIRFLOW_HOME=/workspaces/de-lab/airflow
airflow scheduler &
airflow webserver --port 8080 &
# Open port 8080 → login: admin / admin123
```

### Step 5 — Run dbt Transformations
```bash
cd dbt_project
dbt run
dbt test
dbt docs generate && dbt docs serve
```

### Step 6 — Open Jupyter Notebook
```bash
jupyter notebook --port 8888 --no-browser
# Open port 8888 in browser
```

---

## 📁 Project Structure

```
de-lab/
├── .devcontainer/
│   ├── devcontainer.json     # Codespaces config
│   └── setup.sh              # Auto-install all tools
├── pipelines/
│   └── weather_etl.py        # Main ETL pipeline
├── dags/
│   └── weather_etl_dag.py    # Airflow DAG
├── dbt_project/
│   └── models/
│       ├── staging/          # stg_weather.sql
│       └── marts/            # mart_city_weather_summary.sql
├── notebooks/
│   └── weather_analysis.ipynb
└── README.md
```

---

## 🎯 Interview Talking Points

- **ETL Pipeline** — "Built Python ETL with API ingestion, data validation, and PostgreSQL loading"
- **Airflow** — "Orchestrated pipelines with DAGs, task dependencies, retries, and XCom"
- **dbt** — "Implemented staging → marts layered transformation architecture"
- **Data Quality** — "Added validation checks at ingestion and post-load stages"
- **End-to-End** — "Raw API → warehouse → analytics-ready marts → visualisation"

---

## 🛠️ Tech Stack

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.11 | ETL scripting |
| PostgreSQL | 14 | Data warehouse |
| Apache Airflow | 2.8.1 | Orchestration |
| dbt-postgres | 1.7.0 | Transformation |
| Pandas | 2.1 | Data manipulation |
| Jupyter | Latest | Analysis |

---

*Built by Muhammed Asif T — Data Engineer Portfolio Project*
