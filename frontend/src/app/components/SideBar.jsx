"use client";

import { faArrowRightFromBracket, faPaperPlane  } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import styles from "../../styles/sideBar.module.css";
import Image from "next/image";
import { useChat } from "@/context/ChatContext";
import { useRouter } from "next/navigation";

export default function SideBar(){
	const{chats,selectChat}=useChat();
	const router=useRouter();

	const handleClick=async(chatId)=>{
		await selectChat(chatId);
		router.push("/chat");
	}

	const sortChats = [...chats].sort(
		(a, b) => new Date(b.created_at) - new Date(a.created_at)
	);

	return(
			<aside className={styles.sideBar}>
				<div className={styles.chatListContainer}>
					{sortChats.map((chat)=>(
					<div key={chat.id} className={styles.chatList}>
						<div onClick={()=>handleClick(chat.id)} className={styles.chatItem}>
							<p>Discusion du</p>
							<p className={styles.dateChatList}>{new Date(chat.created_at).toLocaleDateString("fr-FR")}</p>
						</div>
					</div>
					))}
				</div>
			</aside>
	

	)
}