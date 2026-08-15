# AI Disaster Management Platform
## Database Schema

## 1. Database

Primary Database:

PostgreSQL

GIS Extension:

PostGIS

---

# 2. Core Tables

The platform will contain the following main entities:

1. users
2. incidents
3. sos_requests
4. risk_zones
5. rescue_teams
6. vehicles
7. resources
8. shelters
9. hospitals
10. damage_reports
11. alerts
12. road_blockages
13. relief_distributions

---

# 3. Users

Table:

users

Purpose:

Stores citizens, authorities, rescue personnel and administrators.

Fields:

- id
- name
- email
- phone
- password_hash
- role
- created_at
- updated_at

Roles:

- CITIZEN
- AUTHORITY
- RESCUE_TEAM
- ADMIN

---

# 4. Incidents

Table:

incidents

Purpose:

Stores all reported disaster incidents.

Fields:

- id
- title
- description
- disaster_type
- severity
- priority_score
- status
- latitude
- longitude
- reported_by
- created_at
- updated_at

Disaster Types:

- FLOOD
- FIRE
- EARTHQUAKE
- CYCLONE
- LANDSLIDE
- BUILDING_COLLAPSE
- MEDICAL_EMERGENCY
- OTHER

Severity:

- LOW
- MEDIUM
- HIGH
- CRITICAL

Status:

- REPORTED
- VERIFIED
- ASSIGNED
- IN_PROGRESS
- RESOLVED
- CLOSED

---

# 5. SOS Requests

Table:

sos_requests

Purpose:

Stores emergency SOS requests from citizens.

Fields:

- id
- user_id
- incident_id
- emergency_type
- people_count
- latitude
- longitude
- priority_score
- status
- created_at
- resolved_at

Status:

- RECEIVED
- PRIORITIZED
- ASSIGNED
- RESCUE_IN_PROGRESS
- RESCUED
- CANCELLED

---

# 6. Risk Zones

Table:

risk_zones

Purpose:

Stores AI-generated disaster risk areas.

Fields:

- id
- disaster_type
- risk_score
- risk_level
- geometry
- valid_from
- valid_until
- created_at

Risk Levels:

- LOW
- MEDIUM
- HIGH
- CRITICAL

geometry:

PostGIS geometry type.

---

# 7. Rescue Teams

Table:

rescue_teams

Purpose:

Stores emergency rescue teams.

Fields:

- id
- team_name
- team_type
- status
- latitude
- longitude
- contact_number
- capacity
- created_at

Team Types:

- MEDICAL
- FIRE
- POLICE
- FLOOD_RESCUE
- GENERAL_RESCUE

Status:

- AVAILABLE
- ASSIGNED
- EN_ROUTE
- ON_SITE
- UNAVAILABLE

---

# 8. Vehicles

Table:

vehicles

Purpose:

Stores ambulances, fire trucks, rescue vehicles and boats.

Fields:

- id
- vehicle_number
- vehicle_type
- team_id
- status
- latitude
- longitude
- capacity
- created_at

Vehicle Types:

- AMBULANCE
- FIRE_TRUCK
- RESCUE_VEHICLE
- BOAT
- HELICOPTER
- OTHER

---

# 9. Resources

Table:

resources

Purpose:

Tracks emergency resources.

Fields:

- id
- resource_type
- quantity
- unit
- location
- status
- created_at
- updated_at

Resource Types:

- FOOD
- WATER
- MEDICINE
- CLOTHING
- TENT
- BLANKET
- FUEL
- OTHER

---

# 10. Shelters

Table:

shelters

Purpose:

Stores emergency shelters.

Fields:

- id
- name
- address
- latitude
- longitude
- capacity
- current_occupancy
- contact_number
- status
- created_at
- updated_at

Status:

- OPEN
- FULL
- CLOSED
- EMERGENCY_ONLY

---

# 11. Hospitals

Table:

hospitals

Purpose:

Stores hospitals and emergency medical centers.

Fields:

- id
- name
- address
- latitude
- longitude
- emergency_capacity
- available_beds
- contact_number
- status
- created_at
- updated_at

Status:

- OPEN
- FULL
- CLOSED

---

# 12. Damage Reports

Table:

damage_reports

Purpose:

Stores AI-generated damage assessments.

Fields:

- id
- incident_id
- image_url
- damage_type
- damage_level
- confidence_score
- latitude
- longitude
- ai_analysis
- verified
- created_at

Damage Levels:

- NONE
- MINOR
- MODERATE
- SEVERE
- DESTROYED

---

# 13. Alerts

Table:

alerts

Purpose:

Stores disaster warnings and notifications.

Fields:

- id
- title
- message
- alert_type
- severity
- target_area
- created_by
- created_at
- expires_at

Alert Types:

- EARLY_WARNING
- EVACUATION
- WEATHER_WARNING
- EMERGENCY
- RECOVERY

---

# 14. Road Blockages

Table:

road_blockages

Purpose:

Stores blocked or unsafe roads.

Fields:

- id
- road_name
- blockage_type
- severity
- geometry
- reported_by
- status
- created_at
- updated_at

Blockage Types:

- FLOOD
- DEBRIS
- COLLAPSE
- FIRE
- TRAFFIC
- OTHER

Status:

- ACTIVE
- CLEARED
- UNKNOWN

geometry:

PostGIS geometry type.

---

# 15. Relief Distributions

Table:

relief_distributions

Purpose:

Tracks relief materials distributed to affected people or locations.

Fields:

- id
- incident_id
- resource_id
- beneficiary_name
- beneficiary_contact
- quantity
- distributed_by
- distribution_location
- distributed_at
- status

Status:

- PLANNED
- IN_TRANSIT
- DISTRIBUTED
- CANCELLED

---

# 16. Main Relationships

users
    |
    +---- sos_requests
    |
    +---- incidents
    |
    +---- alerts


incidents
    |
    +---- sos_requests
    |
    +---- damage_reports
    |
    +---- relief_distributions


rescue_teams
    |
    +---- vehicles


resources
    |
    +---- relief_distributions

---

# 17. Important Relationships

One user can create many SOS requests.

One incident can have multiple SOS requests.

One incident can have multiple damage reports.

One rescue team can have multiple vehicles.

One resource can be used in multiple relief distributions.

---

# 18. Location Data

All location-sensitive entities should store geographic coordinates.

Latitude:

latitude

Longitude:

longitude

For GIS-enabled entities, use PostGIS geometry.

Examples:

- risk_zones
- road_blockages
- rescue_teams
- vehicles
- shelters
- hospitals

---

# 19. Database Rules

1. Every table must have a primary key.

2. Use foreign keys for relationships.

3. Store passwords only as hashes.

4. Never store plain-text passwords.

5. Use timestamps for important records.

6. Use PostGIS for geographic data.

7. Do not duplicate the same entity in multiple tables.

8. Database changes must be discussed with the backend/integration lead.

9. API responses must use the agreed database structure.

10. Production credentials must never be committed to GitHub.

---

# 20. Future Expansion

The database should be designed so that future modules can be added without major restructuring.

Potential future tables:

- weather_data
- evacuation_centers
- vulnerable_populations
- disaster_predictions
- drone_images
- satellite_images
- emergency_contacts
- volunteer_teams
- insurance_claims
- recovery_projects