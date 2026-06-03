import { faArrowRightFromBracket, faPaperPlane  } from "@fortawesome/free-solid-svg-icons";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import styles from "../../styles/footer.module.css";



export default function Footer(){
	return(
		<footer className={styles.footer}>
			<div className={styles.logout}>
				<FontAwesomeIcon icon={faArrowRightFromBracket} />
					<button className={styles.btnLogout}>Se déconnecter</button>
			</div>
			<div className={styles.inputBar}>
				<input className={styles.input}type="text" placeholder="Tapez votre message ici..." />
				<button className={styles.sendButton}>
					<FontAwesomeIcon icon={faPaperPlane} />
				</button>
			</div>
		</footer>

	)
}