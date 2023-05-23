import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/Twiner.log"),
    ]
)

logger = logging.getLogger("TwinerLog")
