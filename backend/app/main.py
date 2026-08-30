from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from backend.app.database.database import Base, engine

# Import models so SQLAlchemy registers all tables
from backend.app.models.user import User
from backend.app.models.incident import Incident
from backend.app.models.sos import SOSRequest
from backend.app.models.risk_zone import RiskZone
from backend.app.models.rescue_team import RescueTeam
from backend.app.models.vehicle import Vehicle
from backend.app.models.resource import Resource
from backend.app.models.shelter import Shelter
from backend.app.models.hospital import Hospital
from backend.app.models.damage_report import DamageReport
from backend.app.models.alert import Alert
from backend.app.models.road_blockage import RoadBlockage
from backend.app.models.relief_distribution import ReliefDistribution

# Import API routers
from backend.app.routes.users import router as users_router
from backend.app.routes.auth import router as auth_router
from backend.app.routes.incidents import router as incidents_router
from backend.app.routes.sos import router as sos_router
from backend.app.routes.rescue_teams import router as rescue_teams_router
from backend.app.routes.vehicles import router as vehicles_router
from backend.app.routes.resources import router as resources_router
from backend.app.routes.shelters import router as shelters_router
from backend.app.routes.hospitals import router as hospitals_router
from backend.app.routes.risk_zones import router as risk_zones_router
from backend.app.routes.road_blockages import router as road_blockages_router
from backend.app.routes.damage_reports import router as damage_reports_router
from backend.app.routes.alerts import router as alerts_router
from backend.app.routes.relief_distributions import (
    router as relief_distributions_router
)


# Create database tables
Base.metadata.create_all(bind=engine)


# Create FastAPI application
app = FastAPI(
    title="AI Disaster Management Platform",
    description="Backend API for the AI Disaster Management Platform",
    version="1.0.0",
)


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# API ROUTES
# ============================================================

API_PREFIX = "/api/v1"

app.include_router(users_router, prefix=API_PREFIX)
app.include_router(auth_router, prefix=API_PREFIX)
app.include_router(incidents_router, prefix=API_PREFIX)
app.include_router(sos_router, prefix=API_PREFIX)
app.include_router(rescue_teams_router, prefix=API_PREFIX)
app.include_router(vehicles_router, prefix=API_PREFIX)
app.include_router(resources_router, prefix=API_PREFIX)
app.include_router(shelters_router, prefix=API_PREFIX)
app.include_router(hospitals_router, prefix=API_PREFIX)
app.include_router(risk_zones_router, prefix=API_PREFIX)
app.include_router(road_blockages_router, prefix=API_PREFIX)
app.include_router(damage_reports_router, prefix=API_PREFIX)
app.include_router(alerts_router, prefix=API_PREFIX)
app.include_router(relief_distributions_router, prefix=API_PREFIX)


# ============================================================
# ROOT / HEALTH ENDPOINTS
# ============================================================

@app.get(API_PREFIX + "/")
def root():
    return {
        "success": True,
        "message": "AI Disaster Management Platform API is running",
    }


@app.get(API_PREFIX + "/health")
def health():
    return {
        "success": True,
        "status": "healthy",
    }


@app.get(API_PREFIX + "/health/database")
def database_health():
    try:
        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT current_database()")
            )
            database_name = result.scalar()

        return {
            "success": True,
            "database": database_name,
            "status": "connected",
        }

    except Exception as e:
        return {
            "success": False,
            "status": "disconnected",
            "error": str(e),
        }