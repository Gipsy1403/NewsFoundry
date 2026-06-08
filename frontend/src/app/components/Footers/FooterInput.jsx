"use client";

import { useState } from "react";
import { faPaperPlane  } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import styles from "../../../styles/footer.module.css";



export default function FooterInput({onSendMessage, onLogout}){
	const[message, setMessage]=useState("");

	// envoi du message vers la page Chat
	function handleSend(){
		if(!message.trim()) return;
		onSendMessage(message);
		// réinitialisation de l'input
		setMessage("");
	}

	function handleKeyDown(e){
		if(e.key==="Enter"){
			handleSend();
		}
	}
	return(
		<footer className={styles.footer}>
			{/* LOGOUT */}

			{/* INPUT CHAT */}
			<div className={styles.inputBar}>
				<input className={styles.input}type="text" placeholder="Tapez votre message ici..." 
					value={message}
					onChange={(e)=>setMessage(e.target.value)}
					onKeyDown={handleKeyDown}
				/>
				<button className={styles.sendButton} onClick={handleSend}>
					<FontAwesomeIcon icon={faPaperPlane} />
				</button>
			</div>
		</footer>

	)
}