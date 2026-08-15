# AI Disaster Management Platform
## API Contract

## 1. API Rules

Base URL:

/api/v1

All modules communicate through REST APIs.

Authentication:

JWT Bearer Token

Example:

Authorization: Bearer <token>

Response format:

JSON

---

# 2. Standard Response Format

Successful response:

{
  "success": true,
  "data": {},
  "message": "Operation successful"
}

Error response:

{
  "success": false,
  "data": null,
  "message": "Error message"
}

---

# 3. Authentication APIs

## Register

POST /api/v1/auth/register

Request:

{
  "name": "John",
  "email": "john@example.com",
  "phone": "9876543210",
  "password": "password",
  "role": "CITIZEN"
}

Response:

{
  "success": true,
  "data": {
    "user_id": "USR-1001"
  },
  "message": "Registration successful"
}

---

## Login

POST /api/v1/auth/login

Request:

{
  "email": "john@example.com",
  "password": "password"
}

Response:

{
  "success": true,
  "data": {
    "access_token": "JWT_TOKEN",
    "user": {
      "id": "USR-1001",
      "name": "John",
      "role": "CITIZEN"
    }
  },
  "message": "Login successful"
}

---

# 4. User APIs

## Get Current User

GET /api/v1/users/me

Authentication:

Required

Response:

{
  "success": true,
  "data": {
    "id": "USR-1001",
    "name": "John",
    "email": "john@example.com",
    "role": "CITIZEN"
  }
}

---

# 5. SOS APIs

## Create SOS

POST /api/v1/sos

Authentication:

Required

Request:

{
  "emergency_type": "TRAPPED_PERSON",
  "people_count": 5,
  "latitude": 17.98,
  "longitude": 79.59,
  "description": "People trapped inside building"
}

Response:

{
  "success": true,
  "data": {
    "sos_id": "SOS-1001",
    "incident_id": "INC-1001",
    "status": "RECEIVED",
    "priority_score": 0
  },
  "message": "SOS received"
}

---

## Get SOS Status

GET /api/v1/sos/{sos_id}

Authentication:

Required

Response:

{
  "success": true,
  "data": {
    "sos_id": "SOS-1001",
    "status": "RESCUE_IN_PROGRESS",
    "priority_score": 95
  }
}

---

## Get Active SOS Requests

GET /api/v1/sos/active

Authentication:

Authority required

---

# 6. Incident APIs

## Create Incident

POST /api/v1/incidents

Request:

{
  "title": "Flooded Area",
  "description": "Severe flooding reported",
  "disaster_type": "FLOOD",
  "latitude": 17.98,
  "longitude": 79.59
}

---

## Get Incident

GET /api/v1/incidents/{incident_id}

---

## Get Active Incidents

GET /api/v1/incidents/active

---

## Update Incident Status

PATCH /api/v1/incidents/{incident_id}/status

Request:

{
  "status": "IN_PROGRESS"
}

---

# 7. AI Risk Prediction APIs

## Predict Risk

POST /api/v1/ai/risk/predict

Request:

{
  "latitude": 17.98,
  "longitude": 79.59,
  "rainfall": 120,
  "river_level": 4.5,
  "temperature": 28,
  "humidity": 85
}

Response:

{
  "success": true,
  "data": {
    "risk_score": 87,
    "risk_level": "HIGH",
    "disaster_type": "FLOOD",
    "confidence": 0.91
  },
  "message": "Risk prediction generated"
}

Owner:

Member 1

---

# 8. AI Emergency Analysis APIs

## Analyze Emergency Text

POST /api/v1/ai/emergency/analyze-text

Request:

{
  "text": "Five people are trapped inside a flooded building"
}

Response:

{
  "success": true,
  "data": {
    "incident_type": "FLOOD",
    "severity": "CRITICAL",
    "priority_score": 95,
    "confidence": 0.93
  }
}

Owner:

Member 2

---

# 9. AI Image Analysis APIs

## Analyze Image

POST /api/v1/ai/emergency/analyze-image

Content-Type:

multipart/form-data

Input:

image

Response:

{
  "success": true,
  "data": {
    "detected_objects": [
      "PERSON",
      "BUILDING",
      "WATER"
    ],
    "incident_type": "FLOOD",
    "severity": "HIGH",
    "confidence": 0.89
  }
}

Owner:

Member 2

---

# 10. Damage Assessment APIs

## Analyze Damage Image

POST /api/v1/ai/damage/analyze

Content-Type:

multipart/form-data

Input:

image

Response:

{
  "success": true,
  "data": {
    "damage_type": "BUILDING",
    "damage_level": "SEVERE",
    "confidence_score": 0.91
  }
}

Owner:

Member 2

---

# 11. Rescue Team APIs

## Get Available Teams

GET /api/v1/rescue-teams/available

Authentication:

Authority required

Response:

{
  "success": true,
  "data": [
    {
      "id": "TEAM-101",
      "team_name": "Flood Rescue Team 1",
      "team_type": "FLOOD_RESCUE",
      "status": "AVAILABLE",
      "latitude": 17.97,
      "longitude": 79.58
    }
  ]
}

---

## Assign Rescue Team

POST /api/v1/rescue-teams/assign

Request:

{
  "incident_id": "INC-1001",
  "team_id": "TEAM-101"
}

Response:

{
  "success": true,
  "data": {
    "assignment_id": "ASN-1001",
    "status": "ASSIGNED"
  }
}

Owner:

Member 5

---

# 12. GIS APIs

## Find Nearby Rescue Teams

GET /api/v1/gis/nearby-rescue-teams

Parameters:

latitude
longitude
radius

Example:

/api/v1/gis/nearby-rescue-teams?latitude=17.98&longitude=79.59&radius=10

---

## Calculate Safe Route

POST /api/v1/gis/safe-route

Request:

{
  "origin": {
    "latitude": 17.97,
    "longitude": 79.58
  },
  "destination": {
    "latitude": 17.98,
    "longitude": 79.59
  }
}

Response:

{
  "success": true,
  "data": {
    "distance_km": 4.2,
    "estimated_time_minutes": 8,
    "route": []
  }
}

Owner:

Member 6

---

# 13. Risk Zone APIs

## Get Risk Zones

GET /api/v1/gis/risk-zones

Parameters:

disaster_type
risk_level

Example:

/api/v1/gis/risk-zones?disaster_type=FLOOD&risk_level=HIGH

---

# 14. Shelter APIs

## Get Nearby Shelters

GET /api/v1/shelters/nearby

Parameters:

latitude
longitude
radius

Response:

{
  "success": true,
  "data": [
    {
      "id": "SHELTER-101",
      "name": "Emergency Shelter A",
      "latitude": 17.99,
      "longitude": 79.60,
      "capacity": 500,
      "current_occupancy": 320,
      "status": "OPEN"
    }
  ]
}

---

# 15. Hospital APIs

## Get Nearby Hospitals

GET /api/v1/hospitals/nearby

Parameters:

latitude
longitude
radius

---

# 16. Resource APIs

## Get Resources

GET /api/v1/resources

Authentication:

Authority required

---

## Allocate Resource

POST /api/v1/resources/allocate

Request:

{
  "resource_id": "RES-101",
  "incident_id": "INC-1001",
  "quantity": 100
}

---

# 17. Alerts

## Create Alert

POST /api/v1/alerts

Request:

{
  "title": "Flood Warning",
  "message": "Evacuate immediately",
  "alert_type": "EVACUATION",
  "severity": "CRITICAL",
  "target_area": {}
}

---

## Get Active Alerts

GET /api/v1/alerts/active

Authentication:

Optional

---

# 18. Damage Reports

## Create Damage Report

POST /api/v1/damage-reports

Request:

{
  "incident_id": "INC-1001",
  "image_url": "https://example.com/image.jpg",
  "damage_type": "BUILDING",
  "damage_level": "SEVERE",
  "confidence_score": 0.91
}

---

# 19. Road Blockage APIs

## Report Road Blockage

POST /api/v1/road-blockages

Request:

{
  "road_name": "Main Road",
  "blockage_type": "FLOOD",
  "severity": "HIGH",
  "latitude": 17.98,
  "longitude": 79.59
}

---

## Get Active Road Blockages

GET /api/v1/road-blockages/active

---

# 20. Relief APIs

## Create Relief Distribution

POST /api/v1/relief

Request:

{
  "incident_id": "INC-1001",
  "resource_id": "RES-101",
  "beneficiary_name": "John",
  "quantity": 5
}

---

## Get Relief Status

GET /api/v1/relief/{id}

---

# 21. Dashboard APIs

## Authority Dashboard Summary

GET /api/v1/dashboard/summary

Response:

{
  "success": true,
  "data": {
    "active_incidents": 67,
    "critical_sos": 23,
    "available_rescue_teams": 18,
    "available_ambulances": 9,
    "open_shelters": 12
  }
}

Owner:

Member 5

---

# 22. Real-Time Events

WebSocket:

/api/v1/ws

Events:

SOS_CREATED
SOS_UPDATED
INCIDENT_CREATED
INCIDENT_UPDATED
RESCUE_ASSIGNED
RESCUE_STATUS_CHANGED
RISK_ALERT_CREATED
ROAD_BLOCKED
ROAD_CLEARED
DAMAGE_REPORT_CREATED

---

# 23. API Ownership

Member 1:

- AI Risk Prediction

Member 2:

- Emergency AI
- Image Analysis
- Damage Assessment

Member 3:

- Authentication
- Users
- Incidents
- SOS
- Resources
- Shelters
- Hospitals
- Alerts
- Database

Member 4:

- Citizen-facing API integration

Member 5:

- Dashboard
- Rescue Team Assignment
- Resource Allocation

Member 6:

- GIS
- Routing
- Risk Zones
- Location Services

---

# 24. API Development Rules

1. All APIs must use /api/v1.

2. All responses must use the standard response format.

3. Authentication must use JWT.

4. API names must not be changed without team approval.

5. Database IDs must be generated by the backend.

6. AI services must return structured JSON.

7. GIS services must return standardized geographic data.

8. Errors must use HTTP status codes correctly.

9. API documentation must be updated whenever an endpoint changes.

10. Breaking API changes require approval from the integration lead.

11. Never hard-code API keys.

12. Never expose database credentials.

13. Never commit .env files.

---

# 25. Integration Principle

All modules must communicate through the Backend API.

Citizen App
    |
    v
Backend
    |
    +---- AI Services
    |
    +---- GIS Services
    |
    +---- Database
    |
    v
Authority Dashboard

The frontend must not directly access the database.

The frontend should not directly depend on internal AI model implementation.

The AI modules should expose defined service interfaces.

The GIS module should expose defined routing/location interfaces.