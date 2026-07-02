"use client";

import Image from "next/image";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faArrowLeftLong, faBars } from "@fortawesome/free-solid-svg-icons";
import styles from "../../../styles/header.module.css"
import { faFileLines } from "@fortawesome/free-regular-svg-icons";
import { useState } from "react";
import Modal from "../Modal";
import Link from "next/link";
import { useChat } from "@/context/ChatContext";

export default function Header2({ drawerOpen, setDrawerOpen }) {
	const[openModal,setOpenModal]=useState(false)
	const {startNewChat}= useChat();
	const toggleDrawer = () => setDrawerOpen?.((prev) => !prev);

	return (
		<>
			<header className={styles.header}>
				<div className={styles.logoHeader}>
					<button
						className={styles.hamburger}
						onClick={toggleDrawer}
						aria-label={drawerOpen ? "Fermer le menu" : "Ouvrir le menu"}
						aria-expanded={drawerOpen ? "true" : "false"}
						aria-controls="sidebar-navigation"
					>
						<FontAwesomeIcon icon={faBars} aria-hidden="true" />
					</button>
					<Image
						className={styles.logo}
						src="/IMGAppli/logo.png"
						alt="NewsFoundry Logo"
						width={148}
						height={15} />
				</div>
				<div className={styles.barDiscussion}>
					<div className={styles.discussion}>
						<Link href="/home">
							<button className={styles.iconDiscussion} 
								aria-label="Générer une nouvelle discussion"
								onClick={startNewChat}>
								<FontAwesomeIcon icon={faArrowLeftLong} />
							</button>
						</Link>
						<div className={styles.text}>
							<p className={styles.textDiscussion}>Nouvelle discussion</p>
							<p className={styles.textConversation}>Conversation active</p>
						</div>
					</div>
					<button className={styles.btnDiscussion} onClick={() => setOpenModal(true)}>
						<FontAwesomeIcon className={styles.iconGenerate} icon={faFileLines} aria-hidden="true" />
						Générer une revue de presse
					</button>
				</div>
			</header>
			<Modal openModal={openModal} setOpenModal={setOpenModal}/>
		</>
	)
}