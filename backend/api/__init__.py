from backend.api.actions import router as actions_router
from backend.api.admin import router as admin_router
from backend.api.auth import router as auth_router
from backend.api.badges import router as badges_router
from backend.api.carbon import router as carbon_router
from backend.api.ecoverse import router as ecoverse_router
from backend.api.hackathons import router as hackathons_router
from backend.api.leaderboard import router as leaderboard_router
from backend.api.points import router as points_router
from backend.api.projects import router as projects_router
from backend.api.sensors import router as sensors_router
from backend.api.sustainability import router as sustainability_router
from backend.api.teams import router as teams_router
from backend.api.trees import router as trees_router
from backend.api.users import router as users_router
from backend.api.zones import router as zones_router

__all__ = [
    "actions_router",
    "admin_router",
    "auth_router",
    "badges_router",
    "carbon_router",
    "ecoverse_router",
    "hackathons_router",
    "leaderboard_router",
    "points_router",
    "projects_router",
    "sensors_router",
    "sustainability_router",
    "teams_router",
    "trees_router",
    "users_router",
    "zones_router",
]
