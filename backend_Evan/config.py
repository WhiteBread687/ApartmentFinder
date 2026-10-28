"""Settings loaded from backend_Evan/.env; existing environment wins."""
import os
from pathlib import Path
from dotenv import load_dotenv
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')
DATA_MODE = os.getenv('DATA_MODE', 'demo')
DB_CONFIG = dict(host=os.getenv('DB_HOST', 'localhost'),
    port=int(os.getenv('DB_PORT', '3306')), database=os.getenv('DB_NAME', 'apartment_finder'),
    user=os.getenv('DB_USER', 'apartment_app'), password=os.getenv('DB_PASSWORD', ''),
    connection_timeout=5)
