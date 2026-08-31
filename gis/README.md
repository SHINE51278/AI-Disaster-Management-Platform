# GIS Module

## Purpose

The GIS module provides geographic visualization and location-based
functionality for the AI Disaster Management Platform.

## Map Technology

- Frontend: React
- Mapping Library: Leaflet
- React Integration: React Leaflet
- Base Map: OpenStreetMap
- User Location: Browser Geolocation API

## Initial Interactive Map

The initial map supports:

1. Interactive map display
2. Zoom
3. Pan
4. User location marker
5. Incident markers
6. Shelter markers
7. Hospital markers

## Existing Backend APIs

### Active Incidents

GET `/api/v1/incidents/active`

### Risk Zones

GET `/api/v1/gis/risk-zones`

### Nearby Rescue Teams

GET `/api/v1/gis/nearby-rescue-teams`

### Safe Route

POST `/api/v1/gis/safe-route`

### Nearby Shelters

GET `/api/v1/shelters/nearby`

### Nearby Hospitals

GET `/api/v1/hospitals/nearby`

## Architecture

The GIS module communicates with the backend through REST APIs.

Frontend
    ↓
Backend REST API
    ↓
PostgreSQL/PostGIS

The frontend must not directly access the database.

## Current Scope

This task covers the initial interactive disaster map.

Future GIS functionality includes risk zones, rescue-team locations,
road-blockage visualization, routing, distance calculation and ETA.