import os, logging

config = dict(
    DATABASE_PATH=os.getenv("TOUDOU_DATABASE_PATH", ""),
    DATABASE_URL=os.getenv("TOUDOU_DATABASE_URL", ""),
    UPLOAD_FOLDER=os.getenv("TOUDOU_UPLOAD_FOLDER", ""),
    DATA_FOLDER=os.getenv("TOUDOU_DATA_FOLDER", ""),
    LOGS_FOLDER=os.getenv("TOUDOU_LOGS_FOLDER", ""),
    DEBUG=os.getenv("TOUDOU_DEBUG", "False") == "True",
    SECRET_KEY=os.getenv("TOUDOU_SECRET_KEY", "")
)

os.makedirs(config['LOGS_FOLDER'], exist_ok=True)
os.makedirs(config['UPLOAD_FOLDER'], exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(config['LOGS_FOLDER'], "toudou.log")),
        logging.StreamHandler()
    ]
)