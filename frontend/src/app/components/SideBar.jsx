"use client";

import { faArrowRightFromBracket, faPaperPlane  } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import styles from "../../styles/sideBar.module.css";
import Image from "next/image";
import { useChat } from "@/context/ChatContext";

export default function SideBar(){
	const{chats,selectChat}=useChat();

	return(
			<aside className={styles.sideBar}>
				<div className={styles.chatListContainer}>
					{chats.map((chat)=>(
					<div key={chat.id} className={styles.chatList}>
						<div onClick={()=>selectChat(chat.id)} className={styles.chatItem}>
							<p>Discusion du</p>
							<p className={styles.dateChatList}>{new Date(chat.created_at).toLocaleDateString("fr-FR")}</p>
						</div>
					</div>
					))}
				</div>
			</aside>
	

	)
}