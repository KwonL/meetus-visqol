import os

import pymysql
from dotenv import load_dotenv


load_dotenv()

DEBUG = bool(os.environ.get("DEBUG"))
conn = pymysql.connect(
    host=os.environ.get("DB_HOST"),
    user=os.environ.get("DB_USER"),
    port=int(os.environ.get("DB_PORT", 3306)),
    password=os.environ.get("DB_PASSWORD"),
    db="appsol",
)


def save_result_to_db(service: str, mos: float, delay: float):
    if not DEBUG:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO audio_quality (service, mos, delay) VALUE (%s, %s, %s)",
            (service, mos, delay),
        )
        conn.commit()
