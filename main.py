import logging

logging.basicConfig(
    format='%(asctime)s,%(msecs)d %(levelname)s %(name)s:%(lineno)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler()
    ],
    level=logging.INFO
)

logger = logging.getLogger(__name__)

from src.asonumar_handler import AsonumarHandler

if __name__ == "__main__":
    logger.info("Asonumar Gsheet notifier Iniciado!")
    AsonumarHandler().handle()