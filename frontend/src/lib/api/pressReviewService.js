
import { apiFetch } from "./apiFetch";

// transmet l'endpoint /press-reviews pour récupérer la liste des revues de presse
export function getPressReviews() {
  return apiFetch("/press-reviews");
}

// transmet l'endpoint /press-reviews/{id} pour récupérer une revue de presse spécifique
export function getPressReview(id) {
  return apiFetch(`/press-reviews/${id}`);
}

// transmet l'endpoint /press-reviews et la méthode POSTavec body (options de apiFetch) pour créer une nouvelle revue de presse
export function createPressReview(chatId, subject) {
	return apiFetch(`/chats/${chatId}/press-reviews`, {
		method: "POST",
		body: JSON.stringify({ subject }),
	});
}
