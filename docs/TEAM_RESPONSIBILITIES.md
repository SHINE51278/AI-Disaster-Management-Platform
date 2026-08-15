# AI Disaster Management Platform
# Team Responsibilities & Development Rules

## 1. Project Structure

This is ONE project divided into six development modules.

Every member works inside the same GitHub repository:

AI-Disaster-Management-Platform

No member should create a separate independent project.

---

# 2. Team Members

## Member 1 — AI Risk Prediction

### Folder

ai/risk-prediction/

### Responsibility

Build the AI system responsible for predicting disaster risk before a disaster occurs.

### Features

- Disaster risk prediction
- Flood risk prediction
- Risk scoring
- Risk classification
- Environmental data processing
- Historical data processing
- Vulnerability analysis
- Risk-zone generation
- Early-warning prediction

### Input

Environmental and geographic information.

Example:

- rainfall
- river level
- temperature
- humidity
- location
- historical disaster information

### Output

The AI must return structured data.

Example:

{
  "risk_score": 87,
  "risk_level": "HIGH",
  "disaster_type": "FLOOD",
  "confidence": 0.91
}

### API

POST /api/v1/ai/risk/predict

### Deliverables

- Trained model
- Data preprocessing
- Model inference code
- API/service interface
- Test data
- README
- Model documentation

### Do NOT modify

- Citizen frontend
- Authority dashboard
- Main database schema
- Authentication system

---

# 3. Member 2 — AI Emergency & Damage Analysis

### Folder

ai/emergency-analysis/

ai/damage-assessment/

### Responsibility

Build AI systems for analyzing emergency reports and disaster images.

### Emergency Analysis

Features:

- Emergency text classification
- Emergency severity
- Incident classification
- Person detection
- Flood detection
- Fire detection
- Emergency priority scoring

### Damage Assessment

Features:

- Image analysis
- Building detection
- Damage classification
- Damage severity
- Confidence score

### Emergency API

POST /api/v1/ai/emergency/analyze-text

POST /api/v1/ai/emergency/analyze-image

### Damage API

POST /api/v1/ai/damage/analyze

### Example output

{
  "incident_type": "FLOOD",
  "severity": "CRITICAL",
  "priority_score": 95,
  "confidence": 0.93
}

### Deliverables

- AI models
- Preprocessing
- Inference code
- API/service interfaces
- Test images
- Test reports
- README
- Model documentation

### Do NOT modify

- Citizen frontend
- Authority dashboard
- Main database schema
- Authentication system

---

# 4. Member 3 — Backend & Database

### Folder

backend/

database/

### Responsibility

Build the core backend infrastructure.

### Features

- FastAPI server
- REST APIs
- Authentication
- Authorization
- User management
- Incident management
- SOS management
- Resource management
- Shelter management
- Hospital management
- Rescue-team management
- Alert management
- Damage report management
- Relief management
- Database connection
- AI service integration
- GIS service integration
- WebSocket/live updates

### Database

Use:

PostgreSQL + PostGIS

### Main tables

- users
- incidents
- sos_requests
- risk_zones
- rescue_teams
- vehicles
- resources
- shelters
- hospitals
- damage_reports
- alerts
- road_blockages
- relief_distributions

### Deliverables

- Backend server
- Database schema
- Database migrations
- REST APIs
- Authentication
- Authorization
- API documentation
- Seed/demo data
- Automated tests

### Critical responsibility

Member 3 is responsible for maintaining the API contract.

Any breaking API change must be discussed with the integration lead.

---

# 5. Member 4 — Citizen Application

### Folder

frontend/citizen-app/

### Responsibility

Build the citizen-facing application.

### Features

- Registration
- Login
- Home page
- Risk information
- Disaster alerts
- SOS
- Emergency reporting
- Image upload
- Video upload
- GPS location
- Shelter search
- Hospital search
- Evacuation information
- Rescue status
- Relief information

### Main Citizen Flow

Login

↓

Home

↓

View Risk

↓

Receive Alert

↓

Report Emergency / SOS

↓

Upload Image

↓

Track Rescue

↓

View Shelter/Hospital

### APIs used

- Authentication APIs
- SOS APIs
- Incident APIs
- Alert APIs
- Shelter APIs
- Hospital APIs
- GIS APIs
- Rescue status APIs

### Deliverables

- Responsive UI
- API integration
- Location integration
- SOS functionality
- Emergency reporting
- Image upload
- Error handling
- Loading states
- README

### Do NOT

- Directly access the database
- Hard-code API keys
- Create independent backend APIs
- Change API response formats without approval

---

# 6. Member 5 — Authority Command Center

### Folder

frontend/authority-dashboard/

### Responsibility

Build the authority/government command center.

### Features

- Authority login
- Dashboard
- Live incident monitoring
- SOS monitoring
- Emergency prioritization
- Rescue-team monitoring
- Rescue-team assignment
- Ambulance monitoring
- Fire-team monitoring
- Resource monitoring
- Shelter monitoring
- Relief tracking
- Disaster statistics
- Analytics

### Dashboard should display

- Active incidents
- Critical SOS
- High-priority emergencies
- Available rescue teams
- Available ambulances
- Available resources
- Shelter occupancy
- Active alerts

### APIs used

- Dashboard APIs
- Incident APIs
- SOS APIs
- Rescue-team APIs
- Resource APIs
- Shelter APIs
- GIS APIs
- Alert APIs

### Deliverables

- Authority dashboard
- Live incident view
- Interactive map integration
- Rescue assignment UI
- Resource management UI
- Analytics
- API integration
- README

---

# 7. Member 6 — GIS, Routing & Integration

### Folder

gis/

### Responsibility

Build the geographic intelligence and routing system.

### Features

- Interactive map
- GPS
- Geofencing
- Risk-zone visualization
- SOS locations
- Shelter mapping
- Hospital mapping
- Rescue-team locations
- Ambulance locations
- Road blockage mapping
- Safe route calculation
- Rescue routing
- Ambulance routing
- Evacuation routing
- Distance calculation
- ETA calculation

### APIs

GET /api/v1/gis/risk-zones

GET /api/v1/gis/nearby-rescue-teams

POST /api/v1/gis/safe-route

GET /api/v1/shelters/nearby

GET /api/v1/hospitals/nearby

### Deliverables

- Map implementation
- Location services
- Route calculation
- Risk-zone visualization
- Road blockage handling
- GIS service interface
- Test routes
- README

### Do NOT

- Create a separate database
- Create a separate authentication system
- Replace the main backend
- Create a separate application

---

# 8. Shared Rules

## Rule 1 — ONE Repository

Everyone works in:

AI-Disaster-Management-Platform

---

## Rule 2 — ONE Architecture

Everyone follows:

docs/PROJECT_ARCHITECTURE.md

---

## Rule 3 — ONE Database Design

Everyone follows:

docs/DATABASE_SCHEMA.md

---

## Rule 4 — ONE API Contract

Everyone follows:

docs/API_CONTRACT.md

---

## Rule 5 — No Breaking Changes

Do not change:

- API names
- Request format
- Response format
- Database structure

without team approval.

---

# 9. Git Branches

Each member should have a dedicated branch.

Member 1:

member-1-risk-ai

Member 2:

member-2-emergency-ai

Member 3:

member-3-backend

Member 4:

member-4-citizen-app

Member 5:

member-5-command-center

Member 6:

member-6-gis-routing

---

# 10. Git Rules

Never directly push development work to main.

Development flow:

Branch

↓

Code

↓

Test

↓

Commit

↓

Push

↓

Pull Request

↓

Review

↓

Merge

↓

main

---

# 11. Commit Naming

Use meaningful commit messages.

Examples:

feat: add SOS API

feat: add flood risk model

feat: add citizen SOS screen

feat: add command center dashboard

feat: add safe route calculation

fix: correct incident priority

docs: update API contract

---

# 12. Definition of Done

A feature is NOT complete simply because it works on one person's computer.

A feature is complete when:

- Feature implemented
- API integration completed
- Error handling added
- Loading states added
- Authentication handled
- Tests added
- README updated
- Code committed
- Code pushed
- Pull request created
- Integration tested

---

# 13. Integration Requirement

Every member must test their module with the real backend APIs.

Do not rely only on mock data.

Mock data may be used during early development, but real API integration must be completed before final integration.

---

# 14. Communication Rule

If a member needs to change:

- Database schema
- API contract
- Authentication
- Folder structure
- Technology stack
- Shared components

they must inform the integration lead before making the change.

---

# 15. Integration Lead

The integration lead is responsible for:

- Architecture
- GitHub repository
- Branch management
- API contracts
- Database coordination
- Integration testing
- Deployment
- Environment variables
- Final demonstration
- Final SIH presentation

The integration lead does NOT need to write everyone's code.

---

# 16. Final System

The final result must operate as ONE platform.

Citizen

↓

Citizen Application

↓

Backend

↓

AI + GIS + Database

↓

Authority Command Center

↓

Rescue Team

↓

Damage Assessment

↓

Relief Distribution

---

# 17. Final Demonstration Scenario

The complete system should support this demonstration:

1. AI predicts high flood risk.
2. Risk zone appears on the map.
3. Citizen receives warning.
4. Citizen sends SOS.
5. GPS location is captured.
6. Emergency image is uploaded.
7. AI analyzes the image.
8. Emergency priority is calculated.
9. Authority sees the critical incident.
10. GIS finds the nearest rescue team.
11. Safe route is calculated.
12. Authority assigns rescue team.
13. Citizen tracks rescue status.
14. Rescue is completed.
15. Damage image is uploaded.
16. AI assesses damage.
17. Authority tracks affected area.
18. Relief resources are allocated.
19. Distribution is recorded.

This complete flow is the primary integration goal.