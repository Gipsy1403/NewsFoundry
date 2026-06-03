import { faArrowRightFromBracket, faPaperPlane  } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import styles from "../../styles/sideBar.module.css";
import Image from "next/image";



export default function SideBar(){
	return(
			<aside className={styles.sideBar}>

				<div className={styles.chatList}>
					<div className={styles.chatItem}>
						<p>Discusion du</p>
						<p>date</p>
					</div>
				</div>
			</aside>
	

	)
}