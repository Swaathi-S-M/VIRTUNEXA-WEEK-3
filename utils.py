import logging
from datetime import datetime

logging.basicConfig(
    filename="finance_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def get_today_date():
    return datetime.today().strftime("%Y-%m-%d")

def log_action(msg):
    logging.info(msg)
