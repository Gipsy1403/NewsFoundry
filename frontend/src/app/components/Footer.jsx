"use client";

import { useState } from "react";
import {
	faPaperPlane,
	faArrowRightFromBracket,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import styles from "../../styles/footer.module.css";
import { useChat } from "@/context/ChatContext";
import { useRouter } from "next/navigation";

export default function Footer() {
	const [message, setMessage] = useState("");
	const { sendMessage } = useChat();
	const router=useRouter();
	const[inputFocus, setInputFocus]=useState(false);

	async function handleSend() {
		if (!message.trim()) return;
		const content=message;
		setMessage("");
		sendMessage(message);
		router.push("/chat")

		// Réinitialisation de l'input
	}

	function handleKeyDown(e) {
		if (e.key === "Enter" && !e.shiftKey) {
			e.preventDefault();
			handleSend();
		}
	}

	return (
		<footer className={styles.footer}>
			{/* LOGOUT */}
			<div className={styles.logout}>
				<FontAwesomeIcon
					icon={faArrowRightFromBracket}
				/>

				<button
					className={styles.btnLogout}
				>
					Se déconnecter
				</button>
			</div>

			{/* INPUT CHAT */}
			<div className={styles.inputBar}>
				<input
					className={`${styles.input} ${inputFocus ? styles.inputFocus : ""}`}
					type="text"
					placeholder="Tapez votre message ici..."
					value={message}
					onChange={(e) =>
						setMessage(e.target.value)
					}
					onKeyDown={handleKeyDown}
					onFocus={()=>setInputFocus(true)}
					onBlur={()=>setInputFocus(false)}
				/>

				<button
					className={`${styles.sendButton} ${inputFocus ? styles.sendButtonFocused : ""}`}
					onClick={handleSend}
				>
					<FontAwesomeIcon
						icon={faPaperPlane}
					/>
				</button>
			</div>
		</footer>
	);
}