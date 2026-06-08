"use client";

import {createContext,useContext,useEffect,useState} from "react";
import {createChat,sendMessage as apiSendMessage} from "@/lib/api/chatService";

function getCurrentTime() {
	const now = new Date();
	const hours = now.getHours().toString().padStart(2, "0");
	const minutes = now.getMinutes().toString().padStart(2, "0");
	return `${hours}:${minutes}`;
}

const ChatContext = createContext();

	export function ChatProvider({ children }) {
		const [chatId, setChatId] = useState(null);
		const [messages, setMessages] = useState([]);
		const [loading, setLoading] = useState(false);

		async function initChat() {
			try {
				const data = await createChat();

				setChatId(data.chat_id);
			} catch (error) {
				console.error(
					"Erreur création du chat :",
					error
				);
			}
		}
		// Création automatique du chat
		useEffect(() => {
			initChat();
		}, []);

		async function sendMessage(message) {
		if (!message.trim()) return;

		// 1. Message utilisateur avec heure
		const userMessage = {
			role: "user",
			content: message,
			time: getCurrentTime(),
		};

		// Affichage immédiat
		setMessages((prev) => [...prev, userMessage]);

		try {
			setLoading(true);

			const data = await apiSendMessage(chatId, message);

			// 2. On récupère les messages backend
			const backendMessages = data.chat;

			// 3. On ajoute une heure aux messages assistant si absente
			const messagesWithTime = backendMessages.map((msg) => {
				if (!msg.time) {
					return {
						...msg,
						time: getCurrentTime(),
					};
				}
				return msg;
			});

			// 4. Remplacement propre
			setMessages(messagesWithTime);

		} catch (error) {
			console.error("Erreur envoi message :", error);
		} finally {
			setLoading(false);
		}
	}


		return (
			<ChatContext.Provider
				value={{
					messages,
					loading,
					sendMessage,
				}}
			>
				{children}
			</ChatContext.Provider>
		);
	}

export function useChat() {
	return useContext(ChatContext);
}