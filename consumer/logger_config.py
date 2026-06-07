import logging
import sys

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler("oms.log", encoding="utf-8"),
            logging.StreamHandler(sys.stdout)
        ]
    )