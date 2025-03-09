# backend/main.py
from fastapi import FastAPI
from interfaces.api.auth_router import router as auth_router
from interfaces.api.user_router import router as user_router

app = FastAPI()

@app.get("/", include_in_schema=False)  # Ocultar da documentação
async def root():
    return {"message": "Backend rodando com FastAPI!"}

# Registrar os routers
app.include_router(auth_router, prefix="/api", tags=["auth"])
app.include_router(user_router, prefix="/api", tags=["users"])