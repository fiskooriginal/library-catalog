from decimal import Decimal
from os import getenv
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
# Load .env file - environment variables from docker-compose take precedence
# because they are set before this module is loaded
load_dotenv(BASE_DIR / ".env", override=False)

# DEFAULT VALUES FOR DEVELOPMENT PURPOSES ONLY
# DO NOT USE IN PRODUCTION

# database
DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")
DB_NAME = getenv("DB_NAME")
DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")

# open library
OPEN_LIBRARY_BASE_URL = getenv("OPEN_LIBRARY_BASE_URL", "https://openlibrary.org")
OPEN_LIBRARY_COVERS_URL_TEMPLATE = getenv(
    "OPEN_LIBRARY_COVERS_URL_TEMPLATE", "https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
)
OPEN_LIBRARY_SEARCH_PATH = getenv("OPEN_LIBRARY_SEARCH_PATH", "/search.json")
OPEN_LIBRARY_REQUEST_TIMEOUT_SECONDS = int(getenv("OPEN_LIBRARY_REQUEST_TIMEOUT_SECONDS", 5))
OPEN_LIBRARY_SEARCH_LIMIT = int(getenv("OPEN_LIBRARY_SEARCH_LIMIT", 1))
OPEN_LIBRARY_RATING_QUANT = Decimal(getenv("OPEN_LIBRARY_RATING_QUANT", "0.01"))
OPEN_LIBRARY_RATING_MIN = Decimal(getenv("OPEN_LIBRARY_RATING_MIN", "0.00"))
OPEN_LIBRARY_RATING_MAX = Decimal(getenv("OPEN_LIBRARY_RATING_MAX", "9.99"))

# http client
HTTP_SUCCESS_STATUS_MIN = int(getenv("HTTP_SUCCESS_STATUS_MIN", 200))
HTTP_SUCCESS_STATUS_MAX = int(getenv("HTTP_SUCCESS_STATUS_MAX", 203))
HTTP_NO_CONTENT_STATUS = int(getenv("HTTP_NO_CONTENT_STATUS", 204))
HTTP_DEFAULT_ERROR_STATUS = int(getenv("HTTP_DEFAULT_ERROR_STATUS", 400))
HTTP_DEFAULT_SUCCESS_STATUS = int(getenv("HTTP_DEFAULT_SUCCESS_STATUS", 200))
HTTP_METHOD_NOT_ALLOWED_STATUS = int(getenv("HTTP_METHOD_NOT_ALLOWED_STATUS", 405))
HTTP_DEFAULT_ERROR_MESSAGE = getenv("HTTP_DEFAULT_ERROR_MESSAGE", "Oops, something went wrong")

# file storage
JSON_FILE_PATH = getenv("JSON_FILE_PATH", "books.json")

# jsonbin.io
JSONBIN_API_KEY = getenv("JSONBIN_API_KEY", "")
JSONBIN_BIN_ID = getenv("JSONBIN_BIN_ID")

# DEFAULT VALUES FOR DEVELOPMENT PURPOSES ONLY
