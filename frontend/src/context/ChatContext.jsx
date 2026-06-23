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

const ChatContext = createContext();

export function ChatProvider({ children }) {
  const [chatId, setChatId] = useState(null);
  const [messages, setMessages] = useState([]);

//   Liste des conversations disponibles
  const [chats, setChats] = useState([]);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // 📌 sidebar
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

  // Sélectionne une conversation précise
  async function selectChat(id) {
    try {
      setError("");
      const data = await getChat(id);

      setChatId(id);

      // SAFE fallback important
      setMessages(Array.isArray(data?.messages) ? data.messages : []);
      return true;
    } catch (err) {
      console.error(err);
      setError("Impossible de charger cette conversation.");
      setMessages([]);
      return false;
    }
  }

//  Envoi du message à l'assistant
async function sendMessage(message) {
  if (!message?.trim()) return false;

  setError("");
  let currentChatId = chatId;

  if (!currentChatId) {
    const newChat = await createChat();
    currentChatId = newChat.id;
    setChatId(currentChatId);
    setChats((prev) => [newChat, ...prev]);
  }

  const userMessage = {
    role: "user",
    content: message,
    time: new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    }),
  };

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

  // 📌 new chat
  const startNewChat = async () => {
    try {
      setError("");
      const newChat = await createChat();

      setChatId(newChat.id);
      setMessages([]);
      // évite incohérences de cache UI
      setChats((prev) => [newChat, ...prev]);
      return true;
    } catch (err) {
      console.error(err);
      setError("Impossible de démarrer une nouvelle conversation.");
      return false;
    }
  };

  useEffect(() => {
    const init = async () => {
      try {
        setError("");
        const data = await getChats();
        const safeChats = Array.isArray(data) ? data : [];
        setChats(safeChats);
      } catch (err) {
        console.error(err);
        setError("Impossible de charger les conversations.");
        setChats([]);
      }
    };

    init();
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