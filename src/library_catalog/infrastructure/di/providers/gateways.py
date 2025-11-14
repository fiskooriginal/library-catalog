from fastapi import Request

from src.library_catalog.domain.gateways.books import BookMetadataGatewayProtocol
from src.library_catalog.infrastructure.config.settings import OpenLibrarySettings
from src.library_catalog.infrastructure.gateways.open_library import OpenLibraryGateway


def get_open_library_gateway(request: Request) -> BookMetadataGatewayProtocol:
    if not hasattr(request.app.state, "open_library_gateway"):
        raise RuntimeError("OpenLibrary gateway not initialized. Check lifespan configuration.")
    return request.app.state.open_library_gateway


def build_open_library_gateway(settings: OpenLibrarySettings) -> BookMetadataGatewayProtocol:
    return OpenLibraryGateway(settings)
