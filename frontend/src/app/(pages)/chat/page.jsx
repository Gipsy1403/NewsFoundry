"use client";

import styles from "@/styles/chat.module.css";
import Header2 from "@/app/components/Headers/Header2"
import * as Avatar from "@radix-ui/react-avatar";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faUser } from "@fortawesome/free-regular-svg-icons";
import { useChat } from "@/context/ChatContext";
import ReactMarkdown from "react-markdown";
import Loading from "@/app/components/loading";


export default function Chat() {
	const { messages, loading } = useChat();

	return (
		<div className={styles.container}>
			<div className={styles.messages}>
				{messages.map((message, index) =>
					message.role === "user" ? (
						<div
							key={index}
							className={styles.messageRowUser}
						>
							<div className={styles.userMessage}>
								{message.content}
								<p>{message.time}</p>
							</div>

							<Avatar.Root className={`${styles.avatar} ${styles.user}`}>
								<FontAwesomeIcon className={styles.icon} icon={faUser}/>
								<Avatar.Fallback className={styles.Fallback} delayMs={600}/>
							</Avatar.Root>
						</div>
					) : (
						<div
							key={index}
							className={styles.messageRowAssistant}
						>
							<Avatar.Root className={`${styles.avatar} ${styles.assistant}`}>
								<Avatar.Image className={styles.image} src="/IMGAppli/robot.png"/>
								<Avatar.Fallback className={styles.Fallback} delayMs={600}/>
							</Avatar.Root>

							<div className={styles.assistantMessage}>
								<ReactMarkdown>{message.content}</ReactMarkdown>
								<p>{message.time}</p>
							</div>
						</div>
					)
				)}
				{loading && <Loading/>}
			</div>
		</div>
	);
}