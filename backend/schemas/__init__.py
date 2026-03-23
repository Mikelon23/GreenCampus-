from backend.schemas.action import EcoActionCreate, EcoActionResponse
from backend.schemas.auth import AuthLogin, AuthRegister, AuthResponse
from backend.schemas.badge import BadgeResponse
from backend.schemas.carbon import CarbonFootprintCreate, CarbonFootprintResponse
from backend.schemas.hackathon import HackathonCreate, HackathonResponse
from backend.schemas.leaderboard import LeaderboardEntry
from backend.schemas.points import GreenPointsResponse
from backend.schemas.project import ProjectCreate, ProjectResponse
from backend.schemas.sensor import SensorDataCreate, SensorDataResponse
from backend.schemas.sustainability import SustainabilityScoreResponse
from backend.schemas.team import TeamCreate, TeamJoin, TeamResponse
from backend.schemas.tree import TreePlantingCreate, TreePlantingResponse
from backend.schemas.user import UserCreate, UserResponse
from backend.schemas.zone import CampusZoneCreate, CampusZoneResponse

__all__ = [
    "EcoActionCreate",
    "EcoActionResponse",
    "AuthLogin",
    "AuthRegister",
    "AuthResponse",
    "BadgeResponse",
    "CarbonFootprintCreate",
    "CarbonFootprintResponse",
    "HackathonCreate",
    "HackathonResponse",
    "LeaderboardEntry",
    "GreenPointsResponse",
    "ProjectCreate",
    "ProjectResponse",
    "SensorDataCreate",
    "SensorDataResponse",
    "SustainabilityScoreResponse",
    "TeamCreate",
    "TeamJoin",
    "TeamResponse",
    "TreePlantingCreate",
    "TreePlantingResponse",
    "UserCreate",
    "UserResponse",
    "CampusZoneCreate",
    "CampusZoneResponse",
]
