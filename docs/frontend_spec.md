# Frontend Specification

GreenCampus+ Platform

## 1. Overview

The frontend of the GreenCampus+ platform provides the user interface through which students, administrators, and researchers interact with the system.

The interface is designed to present environmental information, sustainability indicators, and community participation tools in a clear and engaging way.

Technology stack:

React
Next.js
TypeScript
Tailwind CSS
Recharts (for data visualization)

The frontend communicates with the backend through REST API endpoints.

---

# 2. Frontend Folder Structure

The frontend project should follow a modular structure.

frontend/

components/
pages/
hooks/
services/
styles/
utils/

Each directory serves a specific purpose.

---

## components/

Contains reusable UI components.

Examples include:

NavigationBar
SidebarMenu
DashboardCard
DataChart
LeaderboardTable
ProjectCard
BadgeDisplay

Components should be reusable across different pages.

---

## pages/

Defines the main views of the application.

Pages correspond to major system modules.

Main pages include:

Dashboard
Carbon Tracker
Green Points
Leaderboard
Campus Sustainability Map
GreenHack Hub
Admin Panel

---

## hooks/

Contains custom React hooks used to manage application state and data fetching.

Examples:

useSensorData
useLeaderboard
useUserPoints
useCarbonData
useHackathons

Hooks should interact with the API services.

---

## services/

Handles communication with the backend API.

Services should include functions for:

fetching environmental data
registering eco-actions
retrieving leaderboard rankings
submitting hackathon projects

API calls should be centralized in this layer.

---

## styles/

Contains styling configuration.

Tailwind CSS should be used for layout and styling.

Custom styles may be added if necessary.

---

## utils/

Contains helper functions.

Examples:

data formatting
date formatting
chart data transformations

---

# 3. Core Frontend Pages

The platform includes several core user interfaces.

---

## Dashboard

The Dashboard provides an overview of sustainability indicators across the campus.

Displayed information includes:

temperature trends
humidity levels
CO₂ concentrations
energy consumption
sustainability score

Data should be visualized using charts and summary cards.

---

## Carbon Tracker

The Carbon Tracker allows users to view and track their carbon footprint.

Features include:

carbon activity history
estimated carbon emissions
environmental impact indicators

Users should be able to register activities affecting their carbon footprint.

---

## Green Points System

This page displays a user's sustainability points and achievements.

Information includes:

total green points
earned badges
recent eco-actions

The system should visually encourage participation.

---

## Leaderboard

The leaderboard ranks users based on sustainability engagement.

Displayed fields:

user name
total points
ranking position

Results should be ordered by total_points.

---

## Campus Sustainability Map

The map visualizes environmental data across different campus zones.

Possible elements include:

sensor locations
temperature distribution
green areas
tree planting zones

Environmental indicators should be associated with campus zones.

---

## GreenHack Hub

This page allows users to participate in sustainability innovation events.

Features include:

viewing hackathon events
creating or joining teams
submitting projects
tracking project impact

Projects submitted through this module are stored in the hackathon database.

---

## Admin Panel

The admin panel allows administrators to manage the platform.

Administrative capabilities include:

creating hackathons
managing campus zones
reviewing environmental indicators
monitoring sustainability metrics

Access to this page should be restricted to admin users.

---

# 4. Data Visualization

Environmental data should be displayed using charts.

Recommended chart types include:

line charts for temperature trends
bar charts for energy consumption
area charts for sustainability indicators

Charts should update dynamically based on API responses.

---

# 5. User Interaction Flow

Typical user interactions include:

viewing environmental indicators
registering eco-actions
tracking personal sustainability metrics
participating in sustainability challenges

These interactions should trigger API requests to the backend services.

---

# 6. Responsiveness

The interface should support multiple screen sizes.

Layouts should adapt to:

desktop screens
tablet devices
mobile devices

Responsive design ensures accessibility across devices.

---

# 7. Performance Considerations

To maintain performance, the frontend should implement:

efficient data fetching
lazy loading of components
optimized chart rendering

Large environmental datasets should be handled efficiently.

---

# 8. Error Handling

Frontend components should gracefully handle API errors.

Possible scenarios include:

failed API requests
network errors
invalid responses

User-friendly error messages should be displayed when necessary.

---

# 9. Future Enhancements

Future improvements may include:

real-time environmental monitoring
interactive campus sustainability maps
AI-driven sustainability recommendations
