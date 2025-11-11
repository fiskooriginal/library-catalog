from dataclasses import dataclass
from decimal import Decimal

from src.library_catalog.infrastructure.config.env import (
    DB_HOST,
    DB_NAME,
    DB_PASSWORD,
    DB_PORT,
    DB_USER,
    HTTP_DEFAULT_ERROR_MESSAGE,
    HTTP_DEFAULT_ERROR_STATUS,
    HTTP_DEFAULT_SUCCESS_STATUS,
    HTTP_METHOD_NOT_ALLOWED_STATUS,
    HTTP_NO_CONTENT_STATUS,
    HTTP_SUCCESS_STATUS_MAX,
    HTTP_SUCCESS_STATUS_MIN,
    JSON_FILE_PATH,
    JSONBIN_API_KEY,
    JSONBIN_BIN_ID,
    OPEN_LIBRARY_BASE_URL,
    OPEN_LIBRARY_COVERS_URL_TEMPLATE,
    OPEN_LIBRARY_RATING_MAX,
    OPEN_LIBRARY_RATING_MIN,
    OPEN_LIBRARY_RATING_QUANT,
    OPEN_LIBRARY_REQUEST_TIMEOUT_SECONDS,
    OPEN_LIBRARY_SEARCH_LIMIT,
    OPEN_LIBRARY_SEARCH_PATH,
)


@dataclass
class DatabaseSettings:
    host: str = DB_HOST
    port: str = DB_PORT
    name: str = DB_NAME
    user: str = DB_USER
    password: str = DB_PASSWORD

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


@dataclass
class HttpClientSettings:
    success_status_min: int = HTTP_SUCCESS_STATUS_MIN
    success_status_max: int = HTTP_SUCCESS_STATUS_MAX
    no_content_status: int = HTTP_NO_CONTENT_STATUS
    default_error_status: int = HTTP_DEFAULT_ERROR_STATUS
    default_success_status: int = HTTP_DEFAULT_SUCCESS_STATUS
    method_not_allowed_status: int = HTTP_METHOD_NOT_ALLOWED_STATUS
    default_error_message: str = HTTP_DEFAULT_ERROR_MESSAGE


@dataclass
class OpenLibrarySettings:
    base_url: str = OPEN_LIBRARY_BASE_URL
    covers_url_template: str = OPEN_LIBRARY_COVERS_URL_TEMPLATE
    search_path: str = OPEN_LIBRARY_SEARCH_PATH
    request_timeout_seconds: int = OPEN_LIBRARY_REQUEST_TIMEOUT_SECONDS
    search_limit: int = OPEN_LIBRARY_SEARCH_LIMIT
    rating_quant: Decimal = OPEN_LIBRARY_RATING_QUANT
    rating_min: Decimal = OPEN_LIBRARY_RATING_MIN
    rating_max: Decimal = OPEN_LIBRARY_RATING_MAX


@dataclass
class FileStorageSettings:
    file_path: str = JSON_FILE_PATH


@dataclass
class JsonBinSettings:
    api_key: str = JSONBIN_API_KEY
    bin_id: str | None = JSONBIN_BIN_ID
