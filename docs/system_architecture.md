# System Architecture

GreenCampus+ Platform

## 1. Architectural Overview

GreenCampus+ follows a modular layered architecture designed to ensure scalability, maintainability, and clear separation of responsibilities.

The system is composed of five main layers:

1. User Layer
2. Frontend Layer
3. API Layer
4. Core Services Layer
5. Data Layer

Each layer has clearly defined responsibilities and communicates through well-defined interfaces.

---

## 2. High-Level Architecture

The interaction between system components follows this flow:

Users
↓
Frontend Application
↓
Backend API
↓
Core Services
↓
Database

Environmental data may also enter the system through simulated or real sensors.

Sensors / Simulation
↓
Backend Data Ingestion
↓
Database
↓
Analytics Services
↓
Dashboard Visualization

---

## 3. User Layer

The User Layer represents the actors interacting with the system.

Primary users include:

Students
Administrators
Researchers

These users access the system through a web-based interface.

---

## 4. Frontend Layer

The Frontend Layer provides the user interface and user experience.

Technology stack:

React
Next.js
TypeScript
Tailwind CSS

Responsibilities:

* Display sustainability dashboards
* Visualize environmental data
* Allow users to register eco-actions
* Provide gamification interfaces
* Manage hackathon participation
* Display campus sustainability indicators

Frontend modules include:

Dashboard
Carbon Tracker
Green Points System
Leaderboard
Campus Sustainability Map
GreenHack Hub
Admin Panel

The frontend communicates with the backend through REST API endpoints.

---

## 5. API Layer

The API Layer acts as the interface between the frontend and the backend logic.

Technology stack:

Python
FastAPI

Responsibilities:

* Receive requests from the frontend
* Validate input data
* Route requests to appropriate services
* Return structured responses

All data exchange occurs through RESTful API endpoints.

Examples include:

/api/sensors
/api/users
/api/actions
/api/carbon
/api/points
/api/hackathons
/api/projects

---

## 6. Core Services Layer

The Core Services Layer contains the main business logic of the system.

Services are designed as independent modules responsible for specific functionality.

Main services include:

Sustainability Engine
Calculates sustainability indicators and environmental performance metrics.

Carbon Analytics Engine
Estimates carbon footprint based on activities and environmental data.

Gamification Engine
Manages points, badges, and leaderboards for sustainability activities.

Hackathon Engine
Handles sustainability challenges, teams, project submissions, and evaluations.

Sensor Data Service
Processes environmental data received from sensors or simulations.

These services interact with the database and provide processed data to the API layer.

---

## 7. Data Layer

The Data Layer stores all persistent data used by the platform.

Technology stack:

PostgreSQL
Supabase

Core data categories include:

User accounts
Environmental sensor data
Sustainability indicators
Carbon footprint metrics
Eco-actions and activity logs
Gamification data (points, badges, rankings)
Hackathon events and project submissions

The database structure is designed to support both real-time monitoring and historical analytics.

---

## 8. Environmental Data Flow

Environmental data can originate from two sources:

1. Physical sensors installed on campus.
2. Simulated environmental data used for development and demonstration.

The data flow follows this pipeline:

Sensors or Simulation
↓
Backend Data Ingestion Service
↓
Database Storage
↓
Analytics Services
↓
Dashboard Visualization

This design ensures that the system can function even without real hardware sensors.

---

## 9. Scalability Considerations

The architecture supports future expansion through modular design.

Possible future extensions include:

IoT integration with real environmental sensors
Machine learning models for sustainability prediction
Integration with university infrastructure systems
Advanced environmental analytics

Each service can be expanded independently without affecting the entire system.

---

## 10. Security Considerations

Basic security practices include:

Authentication and authorization for users
Secure API endpoints
Input validation in backend services
Protection of sensitive user data

Administrative actions are restricted to authorized roles.

---

## 11. Deployment Architecture

The system is designed for cloud deployment using modern hosting platforms.

Frontend deployment:

Vercel

Backend deployment:

Render or Railway

Database:

Supabase PostgreSQL

This architecture enables continuous deployment and scalable cloud infrastructure.
