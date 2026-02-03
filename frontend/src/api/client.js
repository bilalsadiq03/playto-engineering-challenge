const API_BASE = "http://localhost:8000/api";

export async function apiGet(path) {
  const res = await fetch(`${API_BASE}${path}`, {
    credentials: "include",
  });

  if (!res.ok) {
    throw new Error("API GET failed");
  }

  return res.json();
}

export async function apiPost(path) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    credentials: "include",
  });

  if (!res.ok) {
    throw new Error("API POST failed");
  }

  return res.json();
}
