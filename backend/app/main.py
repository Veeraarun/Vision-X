from fastapi import FastAPI
from app.routers import patients

app = FastAPI(title="Vision-X API")

app.include_router(
    patients.router,
    prefix="/api",
    tags=["Patients"]
)

@app.get("/api/health")
def health():
    return {
        "status": "healthy",
        "project": "Vision-X"
    }