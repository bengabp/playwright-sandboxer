from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sandbox.auth import router as auth_router

app = FastAPI(
    title="My Supabase FastAPI Project",
    description="API with Supabase, OAuth2, and Alembic.",
    version="0.1.0",
)

origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Include Routers ---
app.include_router(auth_router.router)

# --- Root Endpoint ---
@app.get("/")
async def root():
    return {"message": "Welcome to the API!"}


