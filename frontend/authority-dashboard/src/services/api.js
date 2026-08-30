const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api/v1";

function getToken() {
  return localStorage.getItem("access_token");
}

async function apiRequest(endpoint, options = {}) {
  const token = getToken();

  const headers = {
    Accept: "application/json",
    ...options.headers,
  };

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const errorText = await response.text();

    throw new Error(
      `API Error ${response.status}: ${errorText || response.statusText}`
    );
  }

  return response.json();
}

export async function getIncidents() {
  return apiRequest("/incidents/active");
}

export async function getSOSRequests() {
  return apiRequest("/sos/active");
}

export async function getRescueTeams() {
  return apiRequest("/rescue-teams");
}

export async function getVehicles() {
  return apiRequest("/vehicles");
}

export async function getResources() {
  return apiRequest("/resources");
}

export async function getShelters() {
  return apiRequest("/shelters");
}

export async function getHospitals() {
  return apiRequest("/hospitals");
}

export async function getRiskZones() {
  return apiRequest("/risk-zones");
}

export async function getAlerts() {
  return apiRequest("/alerts");
}

export async function getReliefDistributions() {
  return apiRequest("/relief-distributions");
}