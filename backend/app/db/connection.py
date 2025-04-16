import os
import oracledb
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    wallet_path = os.getenv("WALLET_PATH")
    return oracledb.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        dsn="webtarhely_high",
        config_dir=wallet_path,
        wallet_location=wallet_path,
        wallet_password=os.getenv("WALLET_PASSWORD")
    )