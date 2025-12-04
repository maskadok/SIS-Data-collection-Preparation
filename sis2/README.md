Technodom Smartphone Data Pipeline.
This project scrapes data about smartphones from the Technodom.kz website, cleans the data, and loads it into a local SQLite database.
The workflow is automated using Apache Airflow 2.9.0.

Website description
https://www.technodom.kz/catalog/smartfony-i-gadzhety/smartfony-i-telefony/smartfony
The website uses dynamic loading, JavaScript rendering, and pagination.
To collect data reliably, the scraper is implemented using Playwright, which loads each catalog page as it appears in the browser.

The scraper collects the following fields:
name,
rating,
number of reviews,
price,
product URL,
category,
raw text extracted from the page.
The cleaned dataset contains 120 smartphone items. 5 pages, 24 cards each.

Project structure
technodom_pipeline/
    airflow_dag.py
    airflow_venv/
    venv/
    src/
        scraper.py
        cleaner.py
        loader.py
    data/
        row_data.csv
        cleaned_data.csv
        output.db
    requirements.txt
    README.md


How to run scraping manually
Activate your Python virtual environment:
  cd ~/Desktop/technodom_pipeline  
  source venv/bin/activate

pip install playwright
playwright install

How to run Airflow
cd ~/Desktop/technodom_pipeline
source airflow_venv/bin/activate

Run the Airflow webserver in one terminal:
airflow webserver

Run the scheduler in another terminal:
airflow scheduler

Open the UI at: http://localhost:8080

Enable the DAG named: technodom_pipeline

To start the pipeline manually, press “Trigger DAG” in the Airflow UI.

The pipeline will run the following tasks in order:
scrape_data
clean_data
load_data

Expected output:
row_data.csv (raw scraped data)
cleaned_data.csv (cleaned dataset for loading)
output.db (SQLite database)

The database contains a table named smartphones with columns:
id
name
rating
reviews
price
product_url
category
raw_text

Each run inserts only new product URLs, so the database grows without duplicates!
