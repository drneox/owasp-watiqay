import argparse
import logging
parser = argparse.ArgumentParser()
parser.add_argument(
    "-log",
    "--log",
    default="warning",
    help=(
        "Provide logging level. "
        "Example --log debug', default='warning'"),
),
options = parser.parse_args()

levels = {
    'critical': logging.CRITICAL,
    'error': logging.ERROR,
    'warn': logging.WARNING,
    'warning': logging.WARNING,
    'info': logging.INFO,
    'debug': logging.DEBUG
}

level = levels.get(options.log.lower())

logging.basicConfig(
    level=level,
    format='%(asctime)s  - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("watiqay.log"),
        logging.StreamHandler()
    ]
)
