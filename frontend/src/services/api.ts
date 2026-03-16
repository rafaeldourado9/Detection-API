const BASE = "/api/v1";

function getToken(): string | null {
  return localStorage.getItem("token");
}

function authHeaders(): HeadersInit {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function register(email: string, password: string) {
  const res = await fetch(`${BASE}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) throw new Error((await res.json()).detail ?? "Registration failed");
  return res.json();
}

export async function login(email: string, password: string) {
  const res = await fetch(`${BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) throw new Error((await res.json()).detail ?? "Login failed");
  return res.json() as Promise<{ access_token: string }>;
}

export async function submitDetection(file: File) {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${BASE}/detections`, {
    method: "POST",
    headers: authHeaders(),
    body: form,
  });
  if (!res.ok) throw new Error("Upload failed");
  return res.json();
}

export async function listDetections() {
  const res = await fetch(`${BASE}/detections`, {
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error("Failed to load detections");
  return res.json();
}

export async function getDetection(id: string) {
  const res = await fetch(`${BASE}/detections/${id}`, {
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error("Detection not found");
  return res.json();
}
