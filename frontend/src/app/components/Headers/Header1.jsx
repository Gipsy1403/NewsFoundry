import Image from "next/image";
import { faComment, faFileLines } from "@fortawesome/free-regular-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import styles from "../../../styles/header.module.css"

export default function Header1() {
	return (
		<header className={styles.header}>
			<div className={styles.logoHeader}>
				<Image
					className={styles.logo}
					src="/IMGAppli/logo.png"
					alt="NewsFoundry Logo"
					width={148}
					height={15} />
			</div>
			<div className={styles.bar}>
				<button className={styles.btn}>
					<FontAwesomeIcon className={styles.icon} icon={faComment} />
					Chat
				</button>
				<button className={styles.btn}>
					<FontAwesomeIcon className={styles.icon} icon={faFileLines} />
					Revue de presse
				</button>
			</div>
		</header>
	)
}