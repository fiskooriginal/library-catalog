from fastapi import FastAPI

from src.library_catalog.endpoints import router

app = FastAPI()

app.include_router(router)


@app.get("/api/health_check")
async def health_check():
    return {"status": "ok"}
