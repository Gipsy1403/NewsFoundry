"use client";

import Image from "next/image";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faArrowLeftLong } from "@fortawesome/free-solid-svg-icons/faArrowLeftLong";
import styles from "../../../styles/header.module.css"
import { faFileLines } from "@fortawesome/free-regular-svg-icons";
import { useState } from "react";
import Modal from "../Modal";
import Link from "next/link";
import { useChat } from "@/context/ChatContext";


export default function Header2() {
	const[openModal,setOpenModal]=useState(false)
	const {startNewChat}= useChat();

	return (
		<>
			<header className={styles.header}>
				<div className={styles.logoHeader}>
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
							<button className={styles.iconDiscussion} aria-roledescription="Générer une nouvelle discussion">
								<FontAwesomeIcon icon={faArrowLeftLong} />
							</button>
						</Link>
						<div className={styles.text}>
							<p className={styles.textDiscussion} onClick={startNewChat}>Nouvelle discussion</p>
							{/* <button className={styles.textDiscussion} onClick={startNewChat}>Nouvelle discussion</button> */}
							<p className={styles.textConversation}>Conversation active</p>
						</div>
					</div>
					<button className={styles.btnDiscussion} onClick={() => setOpenModal(true)}>
						<FontAwesomeIcon className={styles.iconGenerate} icon={faFileLines} />
						Générer une revue de presse
					</button>
				</div>
			</header>
			<Modal openModal={openModal} setOpenModal={setOpenModal}/>
		</>
	)
}