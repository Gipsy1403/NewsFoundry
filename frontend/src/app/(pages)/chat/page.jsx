"use client";

import styles from "@/styles/chat.module.css";
import Header2 from "@/app/components/Headers/Header2"
import * as Avatar from "@radix-ui/react-avatar";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faUser } from "@fortawesome/free-regular-svg-icons";
import { useChat } from "@/context/ChatContext";
import ReactMarkdown from "react-markdown";
import Loading from "@/app/loading";
import { useEffect, useRef } from "react";


export default function Chat() {
	const { messages, loading, error } = useChat();
	const lastMessageRef = useRef(null);

	useEffect(() => {
		if (lastMessageRef.current) {
			lastMessageRef.current.scrollIntoView({
				behavior: "smooth",
				block: "end",
			});

			lastMessageRef.current.focus();
		}
	}, [messages]);
	
	return (
		<div className={styles.container}
			role="log"
			aria-live="polite"
			aria-relevant="additions">
			<div className={styles.messages}>
				{messages.map((message, index) =>
					message.role === "user" ? (
						<div
							key={index}
							className={styles.messageRowUser}
						>
							<div className={styles.userMessage}
								ref={index===messages.length-1 ? lastMessageRef:null}
								tabIndex={0}
								aria-label={`Message utilisateur envoyé à ${message.time}`}>
									{message.content}
								<p className={styles.time}>{message.time}</p>
							</div>

							<Avatar.Root className={`${styles.avatar} ${styles.user}`} aria-hidden="true">
								<FontAwesomeIcon className={styles.icon} icon={faUser} aria-hidden="true"/>
								<Avatar.Fallback className={styles.Fallback} delayMs={600}/>
							</Avatar.Root>
						</div>
					) : (
						<div
							key={index}
							className={styles.messageRowAssistant}
						>
							<Avatar.Root className={`${styles.avatar} ${styles.assistant}`} aria-hidden="true">
								<Avatar.Image className={styles.image} src="/IMGAppli/robot.png" alt=""/>
								<Avatar.Fallback className={styles.Fallback} delayMs={600}/>
							</Avatar.Root>

							<div className={styles.assistantMessage}
								ref={index===messages.length-1 ? lastMessageRef:null}
								tabIndex={0}
								aria-label={`Réponse assistant envoyée à ${message.time}`}>
									<ReactMarkdown>{message.content}</ReactMarkdown>
								<p className={styles.time}>{message.time}</p>
							</div>
						</div>
					)
				)}
				{error && (
					<div className={styles.errorMessage} role="alert">
						{error}
					</div>
				)}
				{loading && <Loading/>}
			</div>
		</div>
	);
}