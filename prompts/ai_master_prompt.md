# GreenCampus+ — Master Development Prompt for Codex

## Role of the AI Agent

You are the primary software development agent responsible for building the **GreenCampus+ platform**, a smart sustainability platform designed to transform universities into intelligent and environmentally responsible ecosystems.

You must analyze the repository structure and implement the project step by step, following the architectural documentation located in the `/docs` directory.

Your goal is to build a **production-ready prototype** that demonstrates environmental monitoring, sustainability analytics, gamification, and green innovation initiatives inside university campuses.

The platform will support real-time environmental monitoring, carbon footprint analytics, gamification systems, and sustainability hackathons.

---

# Project Vision

GreenCampus+ is a **Smart Sustainable Campus Platform** that integrates:

• IoT environmental monitoring
• sustainability analytics
• student engagement through gamification
• carbon footprint tracking
• green hackathons and environmental projects

The platform allows universities to monitor environmental indicators while encouraging students to actively participate in sustainable actions.

---

# Technology Stack

The system must be implemented using the following technologies:

Frontend:

* Next.js
* React
* TypeScript
* TailwindCSS
* Recharts or similar chart library

Backend:

* Python
* FastAPI (preferred) or Flask
* REST API architecture

Database:

* PostgreSQL via Supabase

Infrastructure:

* GitHub (source control)
* Vercel (frontend deployment)
* Render or Railway (backend deployment)
* Supabase (database and authentication)

Optional Tools:

* Docker
* GitHub Actions for CI/CD

---

# Repository Structure

You must follow this repository structure when creating files:

green-campus-plus/

frontend/
backend/
simulation/
infrastructure/
scripts/
tests/
docs/

README.md

Each folder has a specific responsibility.

---

# Documentation Driven Development

Before implementing features, read all files inside the `/docs` directory.

These documents define:

system architecture
database schema
API endpoints
frontend components
business logic

You must use the documentation as the **single source of truth**.

---

# System Architecture

The system follows a modular architecture composed of six layers:

1. User Layer
2. Frontend Layer
3. API Gateway
4. Core Services
5. Data Layer
6. Infrastructure Layer

The frontend communicates with the backend via REST APIs.

The backend processes environmental data and user activity.

The database stores sustainability metrics and user engagement data.

---

# Core Platform Modules

You must implement the following modules.

## 1 Environmental Monitoring Module

Purpose:

Monitor environmental conditions across different campus zones.

Features:

* ingest environmental sensor data
* simulate IoT sensors if real sensors are unavailable
* store temperature, humidity, CO2 and energy data
* visualize trends in the dashboard

Data fields:

temperature
humidity
co2
energy_usage
timestamp
zone_id

---

## 2 Sustainability Dashboard

Create a real-time dashboard that visualizes:

* environmental indicators
* sustainability score
* historical trends
* alerts when thresholds are exceeded

Charts must support:

daily trends
weekly analytics
zone comparisons

---

## 3 Carbon Footprint Tracker

Each user should have an estimated carbon footprint based on activities.

Calculate emissions based on:

transport mode
energy usage
participation in green activities

Display:

weekly footprint
monthly footprint
reduction achievements

---

## 4 Gamification System

Encourage sustainable behaviors through a points system.

Users earn **Green Points** for actions such as:

walking to campus
using bicycles
reporting environmental issues
participating in green events

Gamification features:

leaderboards
badges
levels
eco achievements

---

## 5 Green Hackathon Hub

Create a platform inside the application that allows universities to organize sustainability innovation events.

Hackathon features:

create events
join teams
submit projects
track environmental impact

Each hackathon project should include:

title
description
team members
estimated sustainability impact

---

## 6 Digital Campus Map

Create an interactive map that visualizes:

sensor locations
trees planted
recycling points
sustainable infrastructure

The map should update dynamically with real-time data.

---

# Backend Responsibilities

The backend must implement the following API endpoints:

/api/users
/api/sensors
/api/campus
/api/carbon
/api/points
/api/hackathons
/api/projects

All endpoints must follow RESTful conventions.

Responses should return JSON.

---

# Database Schema

The system must implement the following main tables:

users
campus_zones
sensor_data
sustainability_scores
carbon_footprint
eco_actions
green_points
badges
hackathons
projects
trees_planted

Database migrations should be stored in the repository.

---

# Simulation Engine

Since physical IoT hardware is not required for the prototype, implement a simulation engine that generates environmental data.

The simulation must mimic realistic patterns using:

daily temperature cycles
random noise
human activity patterns

The simulator should send data to the backend API every few seconds.

---

# Development Strategy

The project must be implemented in phases.

Phase 1:
Project scaffolding and base architecture.

Phase 2:
Environmental monitoring and dashboard.

Phase 3:
Gamification system.

Phase 4:
Carbon footprint analytics.

Phase 5:
Green Hackathon Hub.

Phase 6:
Deployment and infrastructure automation.

---

# Code Quality Standards

You must ensure the codebase follows these standards:

modular architecture
clear naming conventions
TypeScript typing on frontend
Python type hints on backend
documentation for all APIs

All functions should include comments explaining their purpose.

---

# Deployment

The system must support the following deployment pipeline:

Frontend → Vercel
Backend → Render or Railway
Database → Supabase

Environment variables must be stored securely.

---

# Final Objective

The final system must demonstrate a working **prototype of a Smart Sustainable Campus Platform** capable of:

monitoring environmental data
analyzing sustainability metrics
engaging students through gamification
organizing green hackathons
tracking environmental impact

The code must be clean, documented, and easy to extend.

Always prioritize clarity, modularity, and scalability.

Begin by analyzing the repository structure and implementing the initial scaffolding for both frontend and backend.
