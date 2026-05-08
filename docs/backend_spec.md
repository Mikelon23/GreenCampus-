# Backend Specification

GreenCampus+ Platform

## 1. Overview

The backend of the GreenCampus+ platform is responsible for handling business logic, processing environmental data, managing user interactions, and providing APIs for the frontend application.

The backend follows a modular service-oriented architecture to ensure maintainability and scalability.

Technology stack:

Python
FastAPI
PostgreSQL (Supabase)

The backend exposes RESTful APIs defined in the API specification document.

---

# 2. Backend Folder Structure

The backend project should follow this folder structure:

backend/

api/
services/
models/
schemas/
utils/
config/

Each directory has a specific responsibility.

---

## api/

Contains route definitions and API endpoints.

Each module should have its own router.

Examples:

users_router
zones_router
sensors_router
actions_router
carbon_router
points_router
hackathons_router

Routers are responsible for:

* receiving requests
* validating input
* calling the appropriate service

---

## services/

Contains the core business logic of the platform.

Services implement the main processing logic used by the API layer.

Main services include:

Sustainability Engine
Carbon Analytics Engine
Gamification Engine
Hackathon Engine
Sensor Data Service

Services interact with the database models and return processed results.

---

## models/

Defines database models corresponding to the tables defined in the database schema.

Each model represents a table in the PostgreSQL database.

Examples:

User
CampusZone
SensorData
EcoAction
CarbonFootprint
GreenPoints
Badge
Hackathon
Team
Project

Models should define:

* fields
* relationships
* constraints

---

## schemas/

Defines request and response data schemas using Pydantic.

Schemas are used for:

input validation
data serialization
API documentation

Examples:

UserCreate
UserResponse
SensorDataCreate
EcoActionCreate
ProjectSubmission

---

## utils/

Contains helper functions and reusable utilities.

Examples:

date utilities
environment calculations
carbon estimation helpers
validation utilities

---

## config/

Contains configuration files and environment settings.

Examples:

database connection configuration
environment variables
application settings

Configuration should support different environments:

development
testing
production

---

# 3. Core Backend Services

The backend is composed of several core services responsible for different aspects of the system.

---

## Sustainability Engine

The Sustainability Engine calculates environmental indicators for campus zones.

Responsibilities include:

calculating sustainability scores
estimating energy efficiency
aggregating environmental sensor data

Inputs:

sensor_data table

Outputs:

sustainability_scores table

These indicators are used in the sustainability dashboard.

---

## Carbon Analytics Engine

The Carbon Analytics Engine estimates carbon footprint metrics based on user activities.

Responsibilities include:

estimating carbon emissions
recording carbon footprint activities
providing carbon analytics to dashboards

Inputs:

eco_actions
carbon_footprint

Outputs:

aggregated carbon impact indicators

---

## Gamification Engine

The Gamification Engine manages user engagement through points and rewards.

Responsibilities include:

assigning points for eco-actions
tracking user scores
updating leaderboards
assigning badges

Inputs:

eco_actions

Outputs:

green_points
user_badges

---

## Hackathon Engine

The Hackathon Engine manages sustainability innovation events.

Responsibilities include:

creating hackathon events
managing teams
tracking project submissions
evaluating impact scores

Inputs:

teams
projects

Outputs:

project impact metrics

---

## Sensor Data Service

This service processes environmental data coming from sensors or simulated sources.

Responsibilities include:

storing sensor readings
validating environmental data
aggregating historical measurements

Sensor data is used by the Sustainability Engine.

---

# 4. Environmental Data Simulation

If physical sensors are not available, the system should support simulated environmental data.

The simulation service should generate realistic environmental data patterns including:

temperature variations
humidity levels
CO₂ concentration
energy consumption

This simulated data can be sent to the sensor ingestion endpoint.

---

# 5. Logging and Monitoring

The backend should implement logging for system monitoring.

Logs should capture:

API requests
errors
environmental data ingestion
system events

Logging improves system observability and debugging.

---

# 6. Error Handling

The backend should implement consistent error handling.

Common error categories include:

validation errors
authentication errors
database errors
unexpected server errors

Error responses should follow the format defined in the API specification.

---

# 7. Security Considerations

Security measures include:

input validation
authentication mechanisms
role-based access control

Administrative endpoints should be protected.

Sensitive operations should require authentication.

---

# 8. Performance Considerations

To support scalability, the backend should implement:

database indexing
efficient query patterns
caching for frequent queries

Large environmental datasets may require optimized queries.

---

# 9. Testing

Backend components should include unit tests.

Tests should cover:

API endpoints
service logic
database operations

Testing ensures reliability and prevents regressions.
