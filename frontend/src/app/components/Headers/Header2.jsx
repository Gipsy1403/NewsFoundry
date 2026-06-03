"use client";

import Image from "next/image";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faArrowLeftLong } from "@fortawesome/free-solid-svg-icons/faArrowLeftLong";
import styles from "../../../styles/header.module.css"
import { faFileLines } from "@fortawesome/free-regular-svg-icons";
import { useState } from "react";
import Modal from "../Modal";


export default function Header2() {
	const[openModal,setOpenModal]=useState(false)
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
						<FontAwesomeIcon className={styles.iconDiscussion} icon={faArrowLeftLong} />
						<div className={styles.text}>
							<p className={styles.textDiscussion}>Nouvelle discussion</p>
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