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
  return apiFetch(`/chats/${chatId}/messages`, {
    method: "POST",
    body: JSON.stringify({ content }),
  });
}