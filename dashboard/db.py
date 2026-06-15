import sqlite3
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parents[1]

sys.path.append(str(BASE_DIR))

from backend.database import initialize_database

initialize_database()

db_path = BASE_DIR / "database" / "vehicle_tracking.db"

def get_connection():
    return sqlite3.connect(
        db_path,
        check_same_thread=False
    )