
import { apiFetch } from "./apiFetch";

export function getPressReviews() {
  return apiFetch("/press-reviews");
}

export function getPressReview(id) {
  return apiFetch(`/press-reviews/${id}`);
}

export function createPressReview(chatId, subject) {
	return apiFetch(`/chats/${chatId}/press-reviews`, {
		method: "POST",
		body: JSON.stringify({ subject }),
	});
}
