import os
from pathlib import Path
import config
from datetime import datetime, timedelta

# Project paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
ROLES_DATA_DIR = DATA_DIR / "roles_data"
UPLOADS_DIR = DATA_DIR / "uploads"

# Create directories if they don't exist
ROLES_DATA_DIR.mkdir(parents=True, exist_ok=True)
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

# Database settings
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./resume_analyzer.db")

# RAG settings
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
VECTOR_DB_PATH = str(DATA_DIR / "vectordb")

# Resume analysis settings
MIN_SIMILARITY_SCORE = 0.3
TOP_CANDIDATES_COUNT = 10

# In your config.py
TESTING_MODE = True  # Set to False in production

# In your application code
if config.TESTING_MODE:
    min_date = datetime.now().date() - timedelta(days=7)  # Allow past dates

# Application settings
SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key-for-session-management")