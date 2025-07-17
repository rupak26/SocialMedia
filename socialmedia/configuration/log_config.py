import logging , os , shutil 
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler
from .log_env import LOG_DIRECTORY , LOG_NAME , ENVIRONMENT as environment 
from logging.handlers import SMTPHandler
from datetime import datetime
from logging import Handler


LOG_PATH = os.path.join(LOG_DIRECTORY, LOG_NAME)
ARCHIVE_DIR = os.path.join(LOG_DIRECTORY, "archive")

MAX_LOG_SIZE = 2 * 1024 * 1024 
BACKUP_COUNT = 30



def log_event(level, message):
    logger = logging.getLogger()
    logger.log(getattr(logging, level.upper()), message)

   
def setup_logging():

    file_handler = TimedRotatingFileHandler(
        filename=LOG_PATH,
        when="midnight",
        interval=1,
        backupCount=7,
        encoding="utf-8",
        utc=True,
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    )
    file_handler.setFormatter(formatter)

    if environment == "development":
        file_handler.setLevel(logging.INFO)
        console_level = logging.INFO
    else:
        file_handler.setLevel(logging.ERROR)
        console_level = logging.ERROR
        log_event("ERROR", "Logger set to ERROR level due to environment")
      

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(console_level)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)  
    root_logger.handlers = []  
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

        


