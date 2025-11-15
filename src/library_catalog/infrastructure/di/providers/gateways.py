from fastapi import Request

from src.library_catalog.domain.gateways.books import BookMetadataGatewayProtocol


def get_open_library_gateway(request: Request) -> BookMetadataGatewayProtocol:
    if not hasattr(request.app.state, "open_library_gateway"):
        raise RuntimeError("OpenLibrary gateway not initialized. Check lifespan configuration.")
    return request.app.state.open_library_gateway
