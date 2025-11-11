from src.library_catalog.domain.gateways.books import BookMetadataGatewayProtocol
from src.library_catalog.infrastructure.config.settings import OpenLibrarySettings
from src.library_catalog.infrastructure.gateways.open_library import OpenLibraryGateway


def get_open_library_gateway() -> BookMetadataGatewayProtocol:
    return OpenLibraryGateway(OpenLibrarySettings())


def build_open_library_gateway(settings: OpenLibrarySettings) -> BookMetadataGatewayProtocol:
    return OpenLibraryGateway(settings)
