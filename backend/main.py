from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from backend.api import (
    actions_router,
    admin_router,
    auth_router,
    badges_router,
    carbon_router,
    ecoverse_router,
    hackathons_router,
    leaderboard_router,
    points_router,
    projects_router,
    sensors_router,
    sustainability_router,
    teams_router,
    trees_router,
    users_router,
    zones_router,
)

app = FastAPI(title="GreenCampus+ API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(zones_router)
app.include_router(sensors_router)
app.include_router(sustainability_router)
app.include_router(carbon_router)
app.include_router(actions_router)
app.include_router(admin_router)
app.include_router(points_router)
app.include_router(leaderboard_router)
app.include_router(badges_router)
app.include_router(hackathons_router)
app.include_router(teams_router)
app.include_router(projects_router)
app.include_router(trees_router)
app.include_router(ecoverse_router)


@app.exception_handler(StarletteHTTPException)
def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """Return consistent error responses for HTTP exceptions."""
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail, "status": exc.status_code})


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Return consistent error responses for validation errors."""
    return JSONResponse(status_code=400, content={"error": "Validation error", "status": 400})


from fastapi.staticfiles import StaticFiles
import os

# Create uploads directory if it doesn't exist
os.makedirs("backend/uploads", exist_ok=True)

app.mount("/uploads", StaticFiles(directory="backend/uploads"), name="uploads")

@app.get("/health")
def health_check() -> dict:
    """Return a simple health check response."""
    return {"status": "ok"}
