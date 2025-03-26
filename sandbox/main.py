from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # Optional: If frontend is on different domain

from app.auth import router as auth_router
# Import routers from other feature packages here
# from app.items import router as items_router

# --- App Initialization ---
app = FastAPI(
    title="My Supabase FastAPI Project",
    description="API with Supabase, OAuth2, and Alembic.",
    version="0.1.0",
)

# --- Middleware --- # Optional: configure CORS
# origins = [
#     "http://localhost",
#     "http://localhost:8080", # Example frontend origin
#     # Add your frontend origins here
# ]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# --- Include Routers ---
app.include_router(auth_router.router)
# app.include_router(items_router.router, prefix="/api/v1") # Example with versioning

# --- Root Endpoint ---
@app.get("/")
async def root():
    return {"message": "Welcome to the API!"}

# --- (Optional) Startup/Shutdown Events ---
# @app.on_event("startup")
# async def startup_event():
#     # Perform actions on startup, e.g., initial db checks
#     pass

# @app.on_event("shutdown")
# async def shutdown_event():
#     # Perform cleanup on shutdown
#     pass
