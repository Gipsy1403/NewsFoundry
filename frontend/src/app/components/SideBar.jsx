"use client";

import { faTimes } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import styles from "../../styles/sideBar.module.css";
import { useChat } from "@/context/ChatContext";
import { useRouter } from "next/navigation";

export default function SideBar({ drawerOpen, setDrawerOpen }){
	const { chats, selectChat } = useChat();
	const router = useRouter();

	const handleClick = async (chatId) => {
		await selectChat(chatId);
		router.push("/chat");
		setDrawerOpen?.(false);
	};

	const closeDrawer = () => setDrawerOpen?.(false);

	const visibleChats = [...chats].sort(
  		(a, b) =>
    		new Date(b.created_at) - new Date(a.created_at)
	);

	return (
		<>
			{drawerOpen && <div className={styles.drawerBackdrop} onClick={closeDrawer} />}
			<aside className={`${styles.sideBar} ${drawerOpen ? styles.open : ""}`}>
				{drawerOpen && (
					<div className={styles.drawerHeader}>
						<button className={styles.closeButton} onClick={closeDrawer} aria-label="Fermer le menu">
							<FontAwesomeIcon icon={faTimes} />
						</button>
					</div>
				)}
				<div className={styles.chatListContainer}>
					{visibleChats.map((chat)=>(
					<div key={chat.id} className={styles.chatList}>
						<div onClick={()=>handleClick(chat.id)} className={styles.chatItem}>
							<p>Discusion du</p>
							<p className={styles.dateChatList}>{new Date(chat.created_at).toLocaleDateString("fr-FR")}</p>
							</div>
						</div>
					))}
				</div>
			</aside>
		</>
	)
}