// Gestionnaire des conversations côté frontend
// Partage les données entre plusieurs composants sans devoir passer des props partout
"use client";

import { createContext, useContext, useEffect, useState } from "react";
import {
  createChat,
  sendMessage as apiSendMessage,
  getChats,
  getChat,
} from "@/lib/api/chatService";


// création du contexte
const ChatContext = createContext();

export function ChatProvider({ children }) {
  const [chatId, setChatId] = useState(null);
  const [messages, setMessages] = useState([]);

  // Liste des conversations disponibles
  const [chats, setChats] = useState([]);
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Recharge la liste des conversations depuis l'API (sidebar)
  async function loadChats() {
    try {
      setError("");
	  const data = await getChats();

      setChats(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error(err);
      setError("Impossible de charger les conversations.");
      setChats([]);
    }
  }

  // charge une conversation précise quand l'utilisateur la sélectionne
  async function selectChat(id) {
    try {
      setError("");
      const data = await getChat(id);

      setChatId(id);

      setMessages(Array.isArray(data?.messages) ? data.messages : []);
      return true;
    } catch (err) {
      console.error(err);
      setError("Impossible de charger cette conversation.");
      setMessages([]);
      return false;
    }
  }

//  Envoi un message utilisateur à l'assistant
async function sendMessage(message) {
  if (!message?.trim()) return false;

  setError("");
  let currentChatId = chatId;

  if (!currentChatId) {
    const newChat = await createChat();
    currentChatId = newChat.id;
    setChatId(currentChatId);
//     ajout de la nouvelle conversation en haut de la sidebar
    setChats((prev) => [newChat, ...prev]);
  }

//    message utilisateur ajouté immédiatement à l'écran
  const userMessage = {
    role: "user",
    content: message,
    time: new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    }),
  };

//  Mise à jour progressive des messages avec le message utilisateur
  setMessages((prev) => [...prev, userMessage]);

  try {
    setLoading(true);

    const data = await apiSendMessage(currentChatId, message);
    await loadChats();

    const assistantMessage = {
      role: "assistant",
      content: data.response,
      time: new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      }),
    };

    setMessages((prev) => [...prev, assistantMessage]);

  } catch (err) {
    console.error(err);
    setError("Impossible d'envoyer le message.");
    return false;
  } finally {
    setLoading(false);
  }
  return true;
}

  // réinitialise l'interface pour commencer une nouvelle conversation
  const startNewChat = () => {
    setError("");
    setChatId(null);
    setMessages([]);
    return true;
  };

// Chargement des conversations au premier affichage du composant.
useEffect(() => {
  async function initChats() {
    await loadChats();
  }
  initChats();
}, []);

  return (
    <ChatContext.Provider
      value={{
        chatId,
        messages,
        chats,
        loading,
        error,
        sendMessage,
        selectChat,
        startNewChat,
        loadChats,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
}

export function useChat() {
  return useContext(ChatContext);
}