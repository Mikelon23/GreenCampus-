# API Specification

GreenCampus+ Platform

## 1. Overview

The GreenCampus+ API provides access to environmental data, sustainability analytics, user actions, and innovation activities.

The API follows RESTful principles and uses JSON for request and response bodies.

Base API path:

/api

Technology stack:

FastAPI (Python)

All endpoints should return structured JSON responses and appropriate HTTP status codes.

---

# 2. Authentication

Authentication is required for most endpoints that modify data and for all personalized endpoints that expose user-specific history or progress.

User roles:

student
admin
researcher

Authentication methods may include:

JWT tokens
session-based authentication

Administrative actions are restricted to users with the admin role.
Personalized endpoints such as carbon history, eco-actions, earned badges, and points must be accessible only to the resource owner or an administrator.

### Auth Endpoints

## POST /api/auth/register

Registers a new user and returns an access token.

Request body:

* name
* email
* role
* password

Response:

* access_token
* user (id, name, email, role, created_at)

---

## POST /api/auth/login

Authenticates an existing user and returns an access token.

Request body:

* email
* password

Response:

* access_token
* user (id, name, email, role, created_at)

---

# 3. User Management

## GET /api/users

Returns a list of users.

Response:

* id
* name
* email
* role
* created_at

---

## GET /api/users/{user_id}

Returns a specific user.

Parameters:

user_id (integer)

---

## POST /api/users

Creates a new user.

Request body:

name
email
role

Note: In the current implementation, end users should use `/api/auth/register` for account creation. `/api/users` is intended for administrative or internal flows.

---

## DELETE /api/users/{user_id}

Deletes a user account.

Access restricted to administrators.

---

# 4. Campus Zones

## GET /api/zones

Returns all campus zones.

Response fields:

id
name
description
location_coordinates

---

## POST /api/zones

Creates a new campus zone.

Admin access required.

---

# 5. Environmental Sensor Data

## GET /api/sensors

Returns environmental sensor data.

Optional query parameters:

zone_id
start_date
end_date

Response fields:

id
zone_id
temperature
humidity
co2_level
energy_usage
timestamp

---

## POST /api/sensors

Registers new sensor data.

This endpoint may be used by:

IoT devices
simulation services

Request body:

zone_id
temperature
humidity
co2_level
energy_usage

---

# 6. Sustainability Indicators

## GET /api/sustainability

Returns sustainability indicators for campus zones.

Response fields:

zone_id
sustainability_score
energy_efficiency_index
carbon_index
calculated_at

---

# 7. Carbon Footprint Tracking

## GET /api/carbon/{user_id}

Returns carbon footprint records for a user.

Access restricted to the resource owner or an administrator.

Response fields:

id
activity_type
carbon_emission_estimate
recorded_at

---

## POST /api/carbon

Registers a carbon footprint activity.

Access restricted to the resource owner or an administrator.

Request body:

user_id
activity_type
carbon_emission_estimate

---

## PUT /api/carbon/{record_id}

Edits a carbon record.

Rules:

* Users can only edit their own record during the first 30 minutes after `recorded_at`.
* Admin users can edit at any time.

Request body:

* activity_type
* carbon_emission_estimate

---

## DELETE /api/carbon/{record_id}

Deletes a carbon record.

Rules:

* Users can only delete their own record during the first 30 minutes after `recorded_at`.
* Admin users can delete at any time.

---

# 8. Eco-Actions

## GET /api/actions/{user_id}

Returns sustainability actions performed by a user.

Access restricted to the resource owner or an administrator.

Response fields:

id
action_type
points_awarded
timestamp

---

## POST /api/actions

Registers a sustainability action.

Access restricted to the resource owner or an administrator.

Request body:

user_id
action_type

Points should be calculated automatically by the gamification engine.

---

## PUT /api/actions/{action_id}

Edits an eco-action.

Rules:

* Users can only edit their own action during the first 30 minutes after `timestamp`.
* Admin users can edit at any time.

Request body:

* action_type
* points_awarded

---

## DELETE /api/actions/{action_id}

Deletes an eco-action.

Rules:

* Users can only delete their own action during the first 30 minutes after `timestamp`.
* Admin users can delete at any time.

---

# 9. Gamification System

## GET /api/points/{user_id}

Returns the total green points of a user.

Access restricted to the resource owner or an administrator.

Response:

user_id
total_points

---

## GET /api/leaderboard

Returns the sustainability leaderboard.

Response fields:

user_id
name
total_points

Results should be sorted by total_points descending.

---

# 10. Hackathons

## GET /api/hackathons

Lists hackathons.

Response fields:

* id
* title
* description
* start_date
* end_date
* status

---

## POST /api/hackathons

Creates a hackathon (admin only).

---

## GET /api/teams

Lists teams. Requires authentication and returns membership state for the current user.

Response fields:

* id
* team_name
* hackathon_id
* created_at
* created_by_user_id
* member_count
* is_member

---

## POST /api/teams

Creates a team for a hackathon (authenticated).

Request body:

* team_name
* hackathon_id

---

## PUT /api/teams/{team_id}

Edits a team.

Rules:

* Only the team creator (or an admin) can edit.
* Edits are allowed during the first 30 minutes after `created_at` unless admin.

---

## DELETE /api/teams/{team_id}

Deletes a team.

Rules:

* Only the team creator (or an admin) can delete.
* Deletes are allowed during the first 30 minutes after `created_at` unless admin.

---

## GET /api/projects

Lists submitted projects.

Response fields:

* id
* team_id
* title
* description
* created_by_user_id
* submission_date
* impact_score
* file_url

---

## POST /api/projects

Submits a project for a team (authenticated).

Request body:

* team_id
* title
* description

---

## PUT /api/projects/{project_id}

Edits a project.

Rules:

* Only the project creator (or an admin) can edit.
* Edits are allowed during the first 30 minutes after `submission_date` unless admin.

---

## DELETE /api/projects/{project_id}

Deletes a project.

Rules:

* Only the project creator (or an admin) can delete.
* Deletes are allowed during the first 30 minutes after `submission_date` unless admin.

---

## POST /api/projects/{project_id}/upload

Uploads an attachment for a project. Requires authentication (team members or admins).

Response includes `file_url`.

---

## GET /api/trees

Lists tree planting records.

Response fields:

* id
* user_id
* zone_id
* tree_species
* planting_date

---

## POST /api/trees

Creates a tree planting record.

Rules:

* Users can only create records for themselves unless admin.

Request body:

* user_id
* zone_id
* tree_species

---

## PUT /api/trees/{tree_id}

Edits a tree record.

Rules:

* Users can only edit their own record during the first 30 minutes after `planting_date`.
* Admin users can edit at any time.

Request body:

* zone_id
* tree_species

---

## DELETE /api/trees/{tree_id}

Deletes a tree record.

Rules:

* Users can only delete their own record during the first 30 minutes after `planting_date`.
* Admin users can delete at any time.

---

# 11. Eco Forest Game (EcoVerse)

## GET /api/ecoverse/overview/{user_id}

Returns the "Eco Forest" overview for the user:

* tree growth stage
* collectable energy drops
* social energy interactions
* streak stats
* campus goals progress

Access restricted to the resource owner or an administrator.

---

## POST /api/ecoverse/energy/{energy_id}/collect

Collects an energy drop for the current user.

---

## POST /api/ecoverse/energy/{energy_id}/help

Helps another user collect energy (social reward).

---

## POST /api/ecoverse/energy/{energy_id}/rescue

Rescues part of an unattended energy drop (optional competitive mechanic).

---

# 12. Admin CRUD

All endpoints require the admin role.

## GET /api/admin/{resource}
## POST /api/admin/{resource}
## PUT /api/admin/{resource}/{item_id}
## DELETE /api/admin/{resource}/{item_id}

Supported resources:

* users
* zones
* sensors
* carbon-records
* eco-actions
* badges
* hackathons
* teams
* projects
* trees
* campus-goals

## GET /api/badges

Returns available sustainability badges.

Response fields:

badge_name
description
points_required

---

## GET /api/badges/earned/{user_id}

Returns badges already earned by a specific user.

Access restricted to the resource owner or an administrator.

Response fields:

badge_name
description
points_required
earned_at

---

# 10. Hackathon Events

## GET /api/hackathons

Returns available sustainability hackathons.

Response fields:

id
title
description
start_date
end_date
status

---

## POST /api/hackathons

Creates a new hackathon event.

Admin access required.

---

# 11. Teams

## GET /api/teams

Returns hackathon teams.

Optional query parameters:

hackathon_id
limit
offset

Access requires authentication.

Response fields:

id
team_name
hackathon_id
created_at
member_count
is_member

---

## POST /api/teams

Creates a team for a hackathon.

The authenticated creator should automatically become the first team member.

Request body:

team_name
hackathon_id

---

## POST /api/teams/{team_id}/join

Adds a user to a team.

Request body:

user_id

Users may only join themselves unless they have administrator access.

---

# 12. Project Submissions

## POST /api/projects

Submits a project to a hackathon.

Access requires authentication.
Non-admin users must belong to the selected team before submitting.

Request body:

team_id
title
description

---

## GET /api/projects

Returns submitted projects.

Response fields:

team_id
title
description
submission_date
impact_score
file_url

---

## POST /api/projects/{project_id}/upload

Uploads a file associated with a submitted project.

Access requires authentication.
Non-admin users must belong to the team that owns the project.

Response fields:

id
team_id
title
description
submission_date
impact_score
file_url

---

# 13. Tree Planting Activities

## POST /api/trees

Registers a tree planting activity.

Request body:

user_id
zone_id
tree_species

---

## GET /api/trees

Returns tree planting records.

Response fields:

user_id
zone_id
tree_species
planting_date

---

# 14. Error Handling

All endpoints should follow consistent error response formats.

Example:

{
"error": "Resource not found",
"status": 404
}

Common HTTP status codes:

200 OK
201 Created
400 Bad Request
401 Unauthorized
404 Not Found
500 Internal Server Error

---

# 15. Pagination and Filtering

Endpoints returning lists should support pagination when data volume increases.

Optional query parameters:

limit
offset

Filtering parameters may be supported depending on the endpoint.
