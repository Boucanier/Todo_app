import os

config = dict(
    DATABASE_PATH=os.getenv("TOUDOU_DATABASE_PATH", ""),
    DATABASE_URL=os.getenv("TOUDOU_DATABASE_URL", ""),
    UPLOAD_FOLDER=os.getenv("TOUDOU_UPLOAD_FOLDER", ""),
    DATA_FOLDER=os.getenv("TOUDOU_DATA_FOLDER", ""),
    DEBUG=os.getenv("TOUDOU_DEBUG", "False") == "True",
    SECRET_KEY=os.getenv("TOUDOU_SECRET_KEY", "")
)