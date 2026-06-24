import { getToken, logout } from "./auth";

// Requêtes API avec gestion du token d'authentification
export async function apiFetch(endpoint, options = {}) {
  const token = getToken();

  const res = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}${endpoint}`,
    {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
        ...options.headers,
      },
    }
  );

  // Intercepte les erreurs 401 pour gérer de manière centralisée les JWT expirés/invalides
  if (res.status === 401) {
    const errorText = await res.text();

    if (typeof window !== "undefined") {
      logout();
      window.location.replace("/login");
    }

    throw new Error(
      `Unauthorized (401): ${errorText || "Token expiré ou invalide"}`
    );
  }

  if (!res.ok) {
    const errorText = await res.text();

    console.error("Status:", res.status);
    console.error("Response:", errorText);

    throw new Error(`API error ${res.status}: ${errorText}`);
  }

  return res.json();
}
