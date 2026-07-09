from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.clothing.routes import router as clothing_router
from app.health.routes import router as health_router
from app.identities.routes import router as identities_router

app = FastAPI(
    title="Smart Wardrobe API",
    summary="FastAPI + MySQL API with a simple learning-friendly structure",
    description=(
        "Small API connected to MySQL using PyMySQL and plain SQL. "
        "Requests flow through routes, API schemas, services, repositories, database connections, and MySQL."
    ),
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://smart-wardrobe-ui-production.up.railway.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(identities_router)
app.include_router(clothing_router)


@app.get("/", tags=["Health"])
def read_root():
    return {"message": "Smart Wardrobe API is running"}
