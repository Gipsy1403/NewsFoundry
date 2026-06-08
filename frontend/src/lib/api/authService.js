import { setToken } from "./auth";

// Service d'authentification
export async function login(email, password) {
  // Appel backend login
console.log("API URL =", process.env.NEXT_PUBLIC_API_URL);
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  });

  // Gestion erreur HTTP
  if (!res.ok) {
    throw new Error("Erreur de connexion");
  }

  const data= await res.json();
  setToken(data.access_token);
  return data;
}
