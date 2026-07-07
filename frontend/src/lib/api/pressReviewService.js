
import { apiFetch } from "./apiFetch";

// Récupère la liste des revues de presse
export function getPressReviews() {
  return apiFetch("/press-reviews");
}

// Récupère une revue de presse spécifique
export function getPressReview(id) {
  return apiFetch(`/press-reviews/${id}`);
}

// Crée une nouvelle revue de presse
export function createPressReview(chatId, subject) {
	return apiFetch(`/chats/${chatId}/press-reviews`, {
		method: "POST",
		body: JSON.stringify({ subject }),
	});
}
