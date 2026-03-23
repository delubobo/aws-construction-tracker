import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./tracker.db")
FRONTEND_ORIGINS: list[str] = os.getenv(
    "FRONTEND_ORIGINS",
    "http://localhost:5173,http://localhost:3000",
).split(",")
