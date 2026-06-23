import Image from "next/image";
import { faComment, faFileLines } from "@fortawesome/free-regular-svg-icons";
import { faBars } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import styles from "../../../styles/header.module.css";
import { usePathname } from "next/navigation";
import Link from "next/link";
import { useChat } from "@/context/ChatContext";

export default function Header1({ drawerOpen, setDrawerOpen }) {
	const pathname=usePathname();
	const isChat=pathname==="/home";
	const isReviewPress=pathname==="/pressreview";
	const {startNewChat}= useChat();
	const toggleDrawer = () => setDrawerOpen?.((prev) => !prev);

	return (
		<header className={styles.header}>
			<div className={styles.logoHeader}>
				<button
					className={styles.hamburger}
					onClick={toggleDrawer}
					aria-label={drawerOpen ? "Fermer le menu" : "Ouvrir le menu"}
					aria-expanded={drawerOpen ? "true" : "false"}
				>
					<FontAwesomeIcon icon={faBars} />
				</button>
				<Image
					className={styles.logo}
					src="/IMGAppli/logo.png"
					alt="NewsFoundry Logo"
					width={148}
					height={15} />
			</div>
			<div className={styles.bar}>
				<Link href="/home">
					<button className={`${styles.btn} ${isChat ? styles.active : styles.disabled}`} onClick={startNewChat}>
						<FontAwesomeIcon className={styles.icon} icon={faComment} />
						Chat
					</button>
				</Link>
				<Link href="/pressreview">
					<button className={`${styles.btn} ${isReviewPress ? styles.active : styles.disabled}`}>
						<FontAwesomeIcon className={styles.icon} icon={faFileLines} />
						Revue de presse
					</button>
				</Link>
			</div>
		</header>
	)
}