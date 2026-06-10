// "use client";

// import { createContext, useContext, useEffect, useState } from "react";
// import {
//   createChat,
//   sendMessage as apiSendMessage,
//   getChats,
//   getChat,
// } from "@/lib/api/chatService";

// const ChatContext = createContext();

// export function ChatProvider({ children }) {
//   const [chatId, setChatId] = useState(null);
//   const [messages, setMessages] = useState([]);
//   const [chats, setChats] = useState([]);
//   const [loading, setLoading] = useState(false);

//   // 1. Charger la liste sidebar
//   async function loadChats() {
//     const data = await getChats();
//     setChats(data);
//   }

//   // 2. Nouveau chat (arrivée page)
//   async function initChat() {
//     const data = await createChat();

//     setChatId(data.id);
// //     setChatId(data.chat_id);
//     setMessages([]);
//   }

//   // 3. Charger un ancien chat
//   async function selectChat(id) {
//     const data = await getChat(id);

//     setChatId(data.id);
//     setMessages(data.messages);
//   }

//   // 4. Envoi message
// async function sendMessage(message) {
// 	if (!message.trim()) return;

// 	if (!chatId) {
// 		console.error("chatId non disponible");
// 		return;
// 	}

// 	const userMessage = {
// 		role: "user",
// 		content: message,
// 	};

// 	setMessages((prev) => [...prev, userMessage]);

// 	try {
// 		setLoading(true);

// 		const data = await apiSendMessage(chatId, message);

// 		console.log(data.chat)
// 		setMessages(data.chat);
// 	} catch (error) {
// 		console.error(error);
// 	} finally {
// 		setLoading(false);
// 	}
// }

// const startNewChat = () => {
//   // 1. sauvegarder l'ancien chat si il existe
//   if (messages.length > 0) {
//     const newChat = {
//       id: crypto.randomUUID(),
//       created_at: new Date(),
//       messages: [...messages],
//     };

//     setChats((prev) => [newChat, ...prev]);
//   }

//   // 2. créer un nouveau chat actif
//   const newActiveId = crypto.randomUUID();
//   setActiveChatId(newActiveId);
//   setMessages([]);
// };
// //   async function sendMessage(message) {

// //     if (!message.trim()) return;

// //     const userMessage = {
// //       role: "user",
// //       content: message,
// //     };

// //     setMessages((prev) => [...prev, userMessage]);

// //     try {
// //       setLoading(true);

// //       const data = await apiSendMessage(chatId, message);

// //       setMessages(data.chat);
// //     } finally {
// //       setLoading(false);
// //     }
// //   }

//   // 5. Init global
//   useEffect(() => {
//     initChat();     // nouveau chat
//     loadChats();    // sidebar
//   }, []);

//   return (
//     <ChatContext.Provider
//       value={{
//         chatId,
//         messages,
//         chats,
//         loading,
//         sendMessage,
//         selectChat,
//         loadChats,
//         initChat,
//       }}
//     >
//       {children}
//     </ChatContext.Provider>
//   );
// }

// export function useChat() {
//   return useContext(ChatContext);
// }

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
  const [messages, setMessages] = useState([]); // ALWAYS array
  const [chats, setChats] = useState([]);       // ALWAYS array
  const [loading, setLoading] = useState(false);

  // 📌 sidebar
  async function loadChats() {
    try {
      const data = await getChats();
      setChats(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error(err);
      setChats([]);
    }
  }

  // 📌 init chat
//   async function initChat() {
//     try {
// 	console.log("INIT CHAT EXECUTED");
//       const data = await createChat();
//       setChatId(data?.id || null);
//       setMessages([]);
//     } catch (err) {
//       console.error(err);
//     }
//   }
// const initChat = async () => {
//   const data = await getChats();

//   const safeChats = Array.isArray(data) ? data : [];

//   setChats(safeChats);

//   if (safeChats.length > 0) {
//     setChatId(safeChats[0].id);
//   }
// };

  // 📌 select chat
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

  // 📌 send message
  async function sendMessage(message) {
    if (!message?.trim()) return;
    if (!chatId) return;

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

      const data = await apiSendMessage(chatId, message);

      // 🔥 IMPORTANT: safe fallback
	const rawMessages = data?.messages || data?.chat || [];

	const newMessages = Array.isArray(rawMessages)
	? rawMessages.map((msg) => ({
		...msg,
		time: msg.time || new Date().toLocaleTimeString([], {
		hour: "2-digit",
		minute: "2-digit",
		}),
	}))
	: [];

      setMessages(Array.isArray(newMessages) ? newMessages : []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  // 📌 new chat
  const startNewChat = async () => {
  const newChat = await createChat();

  setChatId(newChat?.id || null);
  setMessages([]);

  setChats(prev => [newChat, ...prev]);
};

  // 📌 init
//   useEffect(() => {
//     loadChats();
//   }, []);
useEffect(() => {
  const init = async () => {
    const data = await getChats();

    const safeChats = Array.isArray(data) ? data : [];

    setChats(safeChats);

    if (safeChats.length > 0) {
      setChatId(safeChats[0].id);
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