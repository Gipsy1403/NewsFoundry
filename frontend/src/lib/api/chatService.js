import { apiFetch } from "./apiFetch";

export function getChats() {
  return apiFetch("/chats");
}

export function getChat(id) {
  return apiFetch(`/chats/${id}`);
}

export function createChat() {
  return apiFetch("/chats", {
    method: "POST",
  });
}

export function sendMessage(chatId, content) {
	  console.log("sendMessage chatId =", chatId)
	if (!chatId) {
         throw new Error("chatId manquant dans sendMessage")
     }
  return apiFetch(`/chats/${chatId}/messages`, {
    method: "POST",
    body: JSON.stringify({ content }),
  });
}