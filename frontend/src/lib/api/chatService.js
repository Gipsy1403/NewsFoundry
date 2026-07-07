// Centralise tous les appels HTTP liés aux chats

import { apiFetch } from "./apiFetch";

// Récupère la liste des conversations
export function getChats() {
  return apiFetch("/chats");
}

// récupère les messages d'une conversation spécifique
export function getChat(id) {
  return apiFetch(`/chats/${id}`);
}

// Crée une nouvelle conversation
export function createChat() {
  return apiFetch("/chats", {
    method: "POST",
  });
}

// Envoie un message dans une conversation spécifique
export function sendMessage(chatId, content) {

	if (!chatId) {
         throw new Error("chatId manquant dans sendMessage")
     }
  return apiFetch(`/chats/${chatId}/messages`, {
    method: "POST",
    body: JSON.stringify({ content }),
  });
}