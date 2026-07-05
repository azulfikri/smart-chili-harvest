from fastapi import FastAPI
from app.routers.sessions import router as sessions_router

app = FastAPI(
    title="Smart Chili Harvest API"
)

app.include_router(sessions_router)


@app.get("/")
def root():
    return {
        "message": "Backend berjalan 🚀"
    }