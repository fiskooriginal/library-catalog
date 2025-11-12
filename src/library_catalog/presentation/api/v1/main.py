from fastapi import APIRouter

from src.library_catalog.presentation.api.v1.routers.books import router as books_router

router = APIRouter(prefix="/api/v1")

router.include_router(books_router)
