# Gamification System Design

GreenCampus+ Platform

## 1. Overview

The GreenCampus+ platform incorporates a gamification system to motivate sustainable behaviors among campus users.

The system rewards users for participating in environmentally responsible actions such as reducing carbon emissions, joining sustainability initiatives, and contributing to innovation challenges.

Gamification elements include:

green points
badges
leaderboards
achievement levels
eco-energy (collectable energy drops)
virtual tree growth
daily streak loops
collective campus goals
social energy interactions (help and rescue)

These mechanisms encourage continuous engagement with sustainability goals.

---

# 2. Gamification Objectives

The gamification system has several objectives:

encourage sustainable habits
increase user participation in environmental initiatives
reward positive environmental impact
promote friendly competition among students

By integrating gamification with environmental monitoring, the platform connects user behavior with sustainability outcomes.

---

# 3. Green Points System

Green Points represent the primary reward mechanism in the platform.

Users earn points when they perform eco-friendly actions.

Points are accumulated and reflected in the user's profile and leaderboard ranking.

---

## Example Eco-Actions and Points

| Action                                | Points |
| ------------------------------------- | ------ |
| Register eco-friendly transportation  | 20     |
| Participate in a sustainability event | 30     |
| Submit a GreenHack project            | 50     |
| Report environmental issue            | 15     |
| Join tree-planting campaign           | 40     |

Points are stored in the `green_points` field within the user profile.

---

# 3.1 Eco-Energy System (Ant-Forest-Inspired)

In addition to points, users generate "energy" from sustainable actions.

Key rules:

* Energy is created after eco-actions and hackathon submissions.
* Energy appears as collectable drops.
* Energy drops can expire if not collected in time.

Energy provides immediate feedback (short-term reward) and feeds long-term progress (tree growth and campus goals).

---

# 3.2 Social Interaction System

Social interaction strengthens retention and habit formation:

* Help: users can help another player collect an energy drop and receive a smaller bonus.
* Rescue: users can recover part of uncollected energy from other players (optional competitive mechanic).

These interactions create a lightweight social loop without requiring heavy messaging features.

---

# 3.3 Virtual Tree Growth System

Users have a virtual tree that grows based on collected energy.

Tree stages provide visible progress:

* seed
* sprout
* sapling
* young-canopy
* forest-guardian

---

# 3.4 Daily Engagement Loop (Streaks)

To encourage consistency, the system tracks daily streaks:

* current_streak increases when the user performs a daily action (eco-action or energy collection).
* best_streak records the user's longest streak.

Streaks are displayed prominently in the Eco Forest view.

---

# 3.5 Collective Campus Goals

Campus goals are shared targets that progress through collected energy.

When a goal reaches its target, users can be rewarded with points, and the goal can be marked complete.

---

# 4. Badge System

Badges represent achievements obtained by users.

Badges provide recognition for reaching sustainability milestones.

Examples include:

Eco Starter
Green Contributor
Sustainability Champion
Innovation Leader

Badges are awarded automatically when conditions are met.

---

## Example Badge Conditions

| Badge                   | Requirement                |
| ----------------------- | -------------------------- |
| Eco Starter             | Earn first 50 points       |
| Green Contributor       | Earn 200 points            |
| Sustainability Champion | Earn 500 points            |
| Innovation Leader       | Submit a GreenHack project |

Badge data should be stored in the `badges` table.

---

# 5. Leaderboard

The leaderboard ranks users based on their sustainability engagement.

Ranking is calculated using total accumulated green points.

Leaderboard should display:

rank position
user name
total points
earned badges

Leaderboard data should update dynamically as users earn points.

---

# 6. Achievement Levels

In addition to badges, the system may include achievement levels.

Levels provide long-term progression for active users.

Example level structure:

Level 1 - Beginner (0-100 points)
Level 2 - Eco Supporter (100-300 points)
Level 3 - Sustainability Advocate (300-700 points)
Level 4 - Green Leader (700+ points)

Levels should be calculated automatically based on accumulated points.

---

# 7. Gamification Flow

The gamification process follows these steps:

1. User performs an eco-action.
2. The backend validates the action.
3. The system assigns green points.
4. Points are added to the user profile.
5. Badge eligibility is evaluated.
6. Leaderboard ranking is updated.

This process ensures that sustainability activities are consistently rewarded.

---

# 8. Integration with System Components

The gamification system interacts with several platform components.

Backend
Processes eco-actions and assigns points.

Database
Stores points, badges, and leaderboard data.

Frontend
Displays points, achievements, and rankings.

API
Provides endpoints to retrieve gamification data.

---

# 9. Anti-Abuse Considerations

To prevent manipulation of the system, safeguards should be implemented.

Possible measures include:

rate limits for eco-action submissions
verification of environmental activities
admin moderation for event participation

These controls maintain fairness in the leaderboard.

---

# 10. Future Extensions

Future gamification features may include:

team competitions
inter-faculty sustainability rankings
seasonal sustainability challenges
reward redemption systems

These enhancements can further increase user engagement.
