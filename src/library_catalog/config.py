from decimal import Decimal
from os import getenv
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")
DB_NAME = getenv("DB_NAME")
DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")

OPEN_LIBRARY_BASE_URL = "https://openlibrary.org"
OPEN_LIBRARY_COVERS_URL_TEMPLATE = "https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
OPEN_LIBRARY_SEARCH_PATH = "/search.json"
OPEN_LIBRARY_REQUEST_TIMEOUT_SECONDS = 5
OPEN_LIBRARY_SEARCH_LIMIT = 1
OPEN_LIBRARY_RATING_QUANT = Decimal("0.01")
OPEN_LIBRARY_RATING_MIN = Decimal("0.00")
OPEN_LIBRARY_RATING_MAX = Decimal("9.99")

HTTP_SUCCESS_STATUS_MIN = 200
HTTP_SUCCESS_STATUS_MAX = 203
HTTP_NO_CONTENT_STATUS = 204
HTTP_DEFAULT_ERROR_STATUS = 400
HTTP_DEFAULT_SUCCESS_STATUS = 200
HTTP_METHOD_NOT_ALLOWED_STATUS = 405
HTTP_DEFAULT_ERROR_MESSAGE = "Oops, something went wrong"
