import requests
import json
import concurrent.futures
import time
import os
from loguru import logger

logger.add("app.log", level="INFO", format="{time:YYYY-MM-DD HH:mm:ss} | {message}")

def get_ids():
    try:
        res = requests.get('https://github.com/reddelexc/hackerone-reports/raw/master/data.csv')
        if res.status_code == 200:
            csv_data = res.text.split('\n')[1:-1]
            ids = []
            for item in csv_data:
                ids.append(item.split(',')[-4].split('/')[-1])
            logger.info(f"Got {len(ids)} report ids")
            return ids
        else:
            logger.error(f'Failed to get report ids : HTTP ERROR {res.status_code}')
            return None
    except Exception as e:
        logger.error(f'Failed to get report ids due to {e}')
        return None


def download_report(report_id, is_retry=False):
    if report_id in scraped_files:
        logger.info(f"Report {report_id} already scraped. Skipping...")
        return 0
    base_url = "https://hackerone.com/reports/{}.json"
    url = base_url.format(report_id)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        with open(f"json_reports/report_{report_id}.json", "w", encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        logger.info(f"Scraped report {report_id}")
    elif response.status_code == 429:
        logger.error(f"Rate limit exceeded. Failed to scrape report {report_id}")
        time.sleep(60)
        # Retry scraping the report
        if not is_retry:
            download_report(report_id, is_retry=True)
    else:
        logger.critical(f"Failed to scrape report {report_id} with status code {response.status_code}")



# for checking whether the report has been already scraped
scraped_files = os.listdir('json_reports')
scraped_files = [file.split("_")[1].split(".")[0] for file in scraped_files if file.startswith("report_")]

# Number of concurrent requests (adjust as needed)
max_workers = 10
ids = get_ids()

if ids is None:
    logger.critical("Failed to get report ids. Exiting...")
    exit(1)
else:
    logger.info("Starting scraping...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit scraping tasks concurrently
        futures = {executor.submit(download_report, report_id) for report_id in ids}

        # Wait for all tasks to complete
        concurrent.futures.wait(futures)

logger.info("Scraping complete.")