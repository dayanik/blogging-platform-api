import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_URL = 'sqlite+aiosqlite:///' + BASE_DIR / os.getenv("DATABASE_URL")
