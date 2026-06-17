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

  // 📌 sidebar
  async function loadChats() {
    try {
	// Récupère les conversations de l'utilisateur connecté
      const data = await getChats();
	 console.log("CHATS :", data);
      setChats(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error(err);
      setChats([]);
    }
  }

  // Sélectionne une conversation précise
  async function selectChat(id) {
    try {
      const data = await getChat(id);

      setChatId(id);

      // SAFE fallback important
      setMessages(Array.isArray(data?.messages) ? data.messages : []);
    } catch (err) {
      console.error(err);
      setMessages([]);
    }
  }

//  Envoi du message à l'assistant
async function sendMessage(message) {
  if (!message?.trim()) return;

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

    console.log("API RESPONSE :", data);

    const assistantMessage = {
      role: "assistant",
      content: data.response,
      time: new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      }),
    };

    setMessages((prev) => [...prev, assistantMessage]);
//     const assistantMessage = data?.chat?.at(-1);

//     if (assistantMessage) {
//       setMessages((prev) => [
//         ...prev,
//         {
//           role: assistantMessage.role,
//           content: assistantMessage.content,
//           time: new Date().toLocaleTimeString([], {
//             hour: "2-digit",
//             minute: "2-digit",
//           }),
//         },
//       ]);
//     }

  } catch (err) {
    console.error(err);
  } finally {
    setLoading(false);
  }
}

// async function sendMessage(message) {
//   if (!message?.trim()) return;

//   let currentChatId = chatId;

//   // 🧠 CRÉATION AUTOMATIQUE DU CHAT SI INEXISTANT
//   if (!currentChatId) {
//     const newChat = await createChat();
//     currentChatId = newChat.id;
//     setChatId(currentChatId);
//     setChats((prev) => [newChat, ...prev]);
//   }

//   // 🔥 message utilisateur optimiste (UI immédiate)
//   const userMessage = {
//     role: "user",
//     content: message,
//     time: new Date().toLocaleTimeString([], {
//       hour: "2-digit",
//       minute: "2-digit",
//     }),
//   };

//   setMessages((prev) => [...prev, userMessage]);

//   try {
//     setLoading(true);

//     const data = await apiSendMessage(currentChatId, message);

//     console.log("API RESPONSE :", data);

//     const rawMessages =
//       data?.chat || data?.messages || [];

//     // 🧠 sécurisation + format
//     const formattedMessages = Array.isArray(rawMessages)
//       ? rawMessages.map((msg) => ({
//           role: msg.role,
//           content: msg.content,
//           time:
//             msg.time ||
//             new Date().toLocaleTimeString([], {
//               hour: "2-digit",
//               minute: "2-digit",
//             }),
//         }))
//       : [];

//     setMessages((prev) => {
//        const assistantMessage = formattedMessages[formattedMessages.length - 1];
//        return [...prev, assistantMessage];
//     });

//   } catch (err) {
//     console.error(err);
//   } finally {
//     setLoading(false);
//   }
// }

  // 📌 new chat
const startNewChat = async () => {
  try {
    const newChat = await createChat();

    setChatId(newChat.id);

    setMessages([]);
     
    // évite incohérences de cache UI
    setChats((prev) => [newChat, ...prev]);

//     await loadChats();
  } catch (err) {
    console.error(err);
  }
};

useEffect(() => {
  const init = async () => {
    const data = await getChats();

    const safeChats = Array.isArray(data) ? data : [];

    setChats(safeChats);
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