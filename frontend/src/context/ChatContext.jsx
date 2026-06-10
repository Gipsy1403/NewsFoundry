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
  const [chats, setChats] = useState([]);
  const [loading, setLoading] = useState(false);

  // 1. Charger la liste sidebar
  async function loadChats() {
    const data = await getChats();
    setChats(data);
  }

  // 2. Nouveau chat (arrivée page)
  async function initChat() {
    const data = await createChat();

    setChatId(data.id);
//     setChatId(data.chat_id);
    setMessages([]);
  }

  // 3. Charger un ancien chat
  async function selectChat(id) {
    const data = await getChat(id);

    setChatId(data.id);
    setMessages(data.messages);
  }

  // 4. Envoi message
  async function sendMessage(message) {

    if (!message.trim()) return;

    const userMessage = {
      role: "user",
      content: message,
    };

    setMessages((prev) => [...prev, userMessage]);

    try {
      setLoading(true);

      const data = await apiSendMessage(chatId, message);

      setMessages(data.chat);
    } finally {
      setLoading(false);
    }
  }

  // 5. Init global
  useEffect(() => {
    initChat();     // nouveau chat
    loadChats();    // sidebar
  }, []);

  return (
    <ChatContext.Provider
      value={{
        chatId,
        messages,
        chats,
        loading,
        sendMessage,
        selectChat,
        loadChats,
        initChat,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
}

export function useChat() {
  return useContext(ChatContext);
}