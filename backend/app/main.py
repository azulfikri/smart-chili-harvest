from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.sessions import router as sessions_router

app = FastAPI(
    title="Smart Chili Harvest API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Mengizinkan semua origin untuk fase development MVP
    allow_credentials=True,
    allow_methods=["*"], # Mengizinkan semua method (GET, POST, DELETE, dll)
    allow_headers=["*"], # Mengizinkan semua header
)

app.include_router(sessions_router)


@app.get("/")
def root():
    return {
        "message": "Backend berjalan 🚀"
    }