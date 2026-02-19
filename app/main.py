from fastapi import FastAPI
from app.api.cards import router as cards_router

app = FastAPI(
    title="Collection Vault API",
    description="API for managing MTG card collection",
    version="1.0.0"
)

app.include_router(cards_router)

@app.get("/")
def root():
    return {"message": "Welcome to Collection Vault API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}