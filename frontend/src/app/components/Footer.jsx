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
import { logout } from "@/lib/api/token";
import Loading from "@/app/loading";

export default function Footer() {
	const [message, setMessage] = useState("");
	const { sendMessage, loading, error } = useChat();
	const router = useRouter();
	const [inputFocus, setInputFocus] = useState(false);

	async function handleSend() {
		if (!message.trim() || loading) return;

		const success = await sendMessage(message);
		if (!success) return;

		setMessage("");
		router.push("/chat");
	}

	function handleKeyDown(e) {
		if (e.key === "Enter" && !e.shiftKey) {
			e.preventDefault();
			handleSend();
		}
	}

	return (
		<>
			{loading && <Loading/>}
			<footer className={styles.footer}>
				{/* LOGOUT */}
				<div className={styles.logout}>
					<FontAwesomeIcon
						icon={faArrowRightFromBracket}
						aria-hidden="true"
					/>

					<button
						className={styles.btnLogout}
						onClick={() => {
							logout();
							router.push("/login");
						}}
						>
						Se déconnecter
					</button>
				</div>

				{/* INPUT CHAT */}
				<div className={styles.inputBar}>
					<label htmlFor="message" className="srOnly">Message à envoyer</label>
					<input
						className={`${styles.input} ${inputFocus ? styles.inputFocus : ""}`}
						id="message"
						type="text"
						placeholder="Tapez votre message ici..."
						aria-label="Message à envoyer"
						value={message}
						onChange={(e) =>
							setMessage(e.target.value)
						}
						onKeyDown={handleKeyDown}
						onFocus={()=>setInputFocus(true)}
						onBlur={()=>setInputFocus(false)}
					/>

					<button
						type="button"
						className={`${styles.sendButton} ${inputFocus ? styles.sendButtonFocused : ""}`}
						onClick={handleSend}
						disabled={loading || !message.trim()}
						aria-busy={loading}
						aria-label={loading ? "Envoi en cours" : "Envoyer le message"}
					>
						<FontAwesomeIcon
							icon={faPaperPlane}
							aria-hidden="true"
						/>
					</button>
				</div>
				{error && (
					<div className={styles.errorMessage} role="alert">
						{error}
					</div>
				)}
				{loading && <Loading/>}
			</footer>
		</>
	);
}