import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
API_TIMEOUT = 5
DEBUG = os.getenv("DEBUG", "true").lower() == "true"
