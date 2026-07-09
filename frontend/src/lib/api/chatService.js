// Centralise tous les appels HTTP liés aux chats

import { apiFetch } from "./apiFetch";

// transmet l'endpoint /chats pour récupérer la liste des conversations
export function getChats() {
  return apiFetch("/chats");
}

// transmet l'endpoint /chats/{id} pour récupérer les messages d'une conversation spécifique
export function getChat(id) {
  return apiFetch(`/chats/${id}`);
}

// transmet l'endpoint /chats et la méthode POST (options de apiFetch) pour créer une nouvelle conversation
export function createChat() {
  return apiFetch("/chats", {
    method: "POST",
  });
}

// transmet l'endpoint /chats/{id}/messages et la méthode POST avec le body (options de apiFetch) pour envoyer un message dans une conversation spécifique
export function sendMessage(chatId, content) {

	if (!chatId) {
         throw new Error("chatId manquant dans sendMessage")
     }
  return apiFetch(`/chats/${chatId}/messages`, {
    method: "POST",
    body: JSON.stringify({ content }),
  });
}