// "use client";

// import { useState } from "react";
// import { faPaperPlane, faArrowRightFromBracket  } from "@fortawesome/free-solid-svg-icons";
// import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
// import styles from "../../styles/footer.module.css";



// export default function Footer({onSendMessage}){
// 	const[message, setMessage]=useState("");

// 	// envoi du message vers la page Chat
// 	function handleSend(){
// 		if(!message.trim()) return;
// 		onSendMessage(message);
// 		// réinitialisation de l'input
// 		setMessage("");
// 	}

// 	function handleKeyDown(e){
// 		if(e.key==="Enter"){
// 			handleSend();
// 		}
// 	}
// 	return(
// 		<footer className={styles.footer}>
// 			{/* LOGOUT */}
// 			<div className={styles.logout}>
// 				<FontAwesomeIcon icon={faArrowRightFromBracket} />
// 					<button className={styles.btnLogout}>Se déconnecter</button>
// 			</div>
// 			{/* INPUT CHAT */}
// 			<div className={styles.inputBar}>
// 				<input className={styles.input}type="text" placeholder="Tapez votre message ici..." 
// 					value={message}
// 					onChange={(e)=>setMessage(e.target.value)}
// 					onKeyDown={handleKeyDown}
// 				/>
// 				<button className={styles.sendButton} onClick={handleSend}>
// 					<FontAwesomeIcon icon={faPaperPlane} />
// 				</button>
// 			</div>
// 		</footer>

// 	)
// }

"use client";

import { useState } from "react";

import {
	faPaperPlane,
	faArrowRightFromBracket,
} from "@fortawesome/free-solid-svg-icons";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import styles from "../../styles/footer.module.css";

import { useChat } from "@/context/ChatContext";

export default function Footer() {
	const [message, setMessage] = useState("");

	const { sendMessage } = useChat();

	async function handleSend() {
		if (!message.trim()) return;

		await sendMessage(message);

		// Réinitialisation de l'input
		setMessage("");
	}

	function handleKeyDown(e) {
		if (e.key === "Enter") {
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
					className={styles.input}
					type="text"
					placeholder="Tapez votre message ici..."
					value={message}
					onChange={(e) =>
						setMessage(e.target.value)
					}
					onKeyDown={handleKeyDown}
				/>

				<button
					className={styles.sendButton}
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