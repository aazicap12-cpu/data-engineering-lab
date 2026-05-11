#!/bin/bash
set -e

echo "=========================================="
echo "  Data Engineering Lab — Setup Starting"
echo "=========================================="

# Install PostgreSQL
sudo apt-get update -qq
sudo apt-get install -y postgresql postgresql-contrib

# Start PostgreSQL
sudo service postgresql start
sleep 3

# Create DB and user
sudo -u postgres psql -c "CREATE USER deuser WITH PASSWORD 'depass123';" 2>/dev/null || true
sudo -u postgres psql -c "CREATE DATABASE de_lab OWNER deuser;" 2>/dev/null || true
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE de_lab TO deuser;" 2>/dev/null || true

echo "✅ PostgreSQL ready — de_lab database created"

# Install Python packages
pip install --quiet \
  apache-airflow==2.8.1 \
  dbt-postgres==1.7.0 \
  pandas==2.1.0 \
  numpy==1.26.0 \
  sqlalchemy==1.4.50 \
  psycopg2-binary \
  requests \
  python-dotenv \
  jupyter \
  matplotlib \
  seaborn \
  great-expectations

echo "✅ Python packages installed"

# Init Airflow
export AIRFLOW_HOME=/workspaces/de-lab/airflow
mkdir -p $AIRFLOW_HOME

airflow db init 2>/dev/null
airflow users create \
  --username admin \
  --firstname Asif \
  --lastname T \
  --role Admin \
  --email asifthiruthy@gmail.com \
  --password admin123 2>/dev/null || true

echo "✅ Airflow initialised"

# Init dbt
cd /workspaces/de-lab/dbt_project
dbt init . --skip-profile-setup 2>/dev/null || true

echo ""
echo "=========================================="
echo "  ✅ Setup Complete! All tools ready."
echo "  PostgreSQL : localhost:5432 / de_lab"
echo "  Airflow UI : localhost:8080 (admin/admin123)"
echo "  Jupyter    : run 'jupyter notebook --port 8888'"
echo "=========================================="
