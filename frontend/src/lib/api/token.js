// Gestion du token d'authentification dans le localStorage

// enregistre le JWT dans le local storage après l'authentification réussie
export function setToken(token) {
  if (typeof window !== "undefined") {
    localStorage.setItem("token", token);
  }
}

// Récupère le JWT enregistré dans le local storage
export function getToken() {
  if (typeof window !== "undefined") {
    return localStorage.getItem("token");
  }
  return null;
}

// Supprime le JWT du local storage à la déconnection de l'utilisateur
export function logout() {
  if (typeof window !== "undefined") {
    localStorage.removeItem("token");
  }
}