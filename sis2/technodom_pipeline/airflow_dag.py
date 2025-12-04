from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import subprocess
import sys
import os

# Папка проекта — ПРОВЕРЬ, ЧТО ОНА ТОЧНАЯ!
PROJECT_DIR = "/Users/admin/Desktop/technodom_pipeline"
SRC_DIR = os.path.join(PROJECT_DIR, "src")

SCRAPER = os.path.join(SRC_DIR, "scraper.py")
CLEANER = os.path.join(SRC_DIR, "cleaner.py")
LOADER = os.path.join(SRC_DIR, "loader.py")


def run_script(path: str):
    """Запуск python-скрипта внутри того же окружения, что и Airflow."""
    result = subprocess.run(
        [sys.executable, path],  # <-- ВАЖНО: использует airflow_venv/bin/python
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Error running {path}:\nSTDERR:\n{result.stderr}\n"
        )

    print(result.stdout)


default_args = {
    "owner": "airflow",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="technodom_pipeline",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval=timedelta(days=1),
    catchup=False,
) as dag:

    scrape_task = PythonOperator(
        task_id="scrape_data",
        python_callable=run_script,
        op_kwargs={"path": SCRAPER},
    )

    clean_task = PythonOperator(
        task_id="clean_data",
        python_callable=run_script,
        op_kwargs={"path": CLEANER},
    )

    load_task = PythonOperator(
        task_id="load_data",
        python_callable=run_script,
        op_kwargs={"path": LOADER},
    )

    scrape_task >> clean_task >> load_task
