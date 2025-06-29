const API_URL = "http://localhost:8000";

export async function login(username, password) {
  const response = await fetch(`${API_URL}/token`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({ username, password })
  });
  if (!response.ok) throw new Error("Login failed");
  return response.json();
}

export async function registerStudent(data, token) {
  const response = await fetch(`${API_URL}/registrations/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify(data)
  });
  if (!response.ok) throw new Error("Registration failed");
  return response.json();
}

export async function getRegistrations(token) {
  const response = await fetch(`${API_URL}/registrations/`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  if (!response.ok) throw new Error("Failed to fetch registrations");
  return response.json();
}