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
			<aside id="sidebar-navigation" className={`${styles.sideBar} ${drawerOpen ? styles.open : ""}`} aria-label="Historique des conversations">
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
						<button
							type="button"
							onClick={() => handleClick(chat.id)}
							className={styles.chatItem}
							aria-label={`Ouvrir la conversation du ${new Date(chat.created_at).toLocaleDateString("fr-FR")}`}
						>
							<p>Discusion du</p>
							<p className={styles.dateChatList}>{new Date(chat.created_at).toLocaleDateString("fr-FR")}</p>
						</button>
						</div>
					))}
				</div>
			</aside>
		</>
	)
}