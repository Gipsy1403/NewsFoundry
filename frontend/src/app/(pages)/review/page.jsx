import { faCalendar } from "@fortawesome/free-regular-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import styles from "../../../styles/pressreview.module.css"

export default function ReviewPress() {
	return (
		<article className={styles.containerPress} >
			<p className={styles.title}>Revues de Presse</p>
			<p className={styles.subTitle}>Consultez et gérez vos revues de presse générées par l'IA</p>
			<div className={styles.card}>
				<div className={styles.headerCard}>
					<div>
						<p className={styles.titleCard}>titre + semaine</p>
						<div className={styles.dateCard}>
							<FontAwesomeIcon className={styles.iconCard} icon={faCalendar} />date
						</div>
					</div>
					<button className={styles.btnCard}>Copier</button>
				</div>
				<div className={styles.article}>
					<div className={styles.titleArticle}>
						<p className={styles.titlePress}>revue de presse</p>
						<p className={styles.datePress}>date</p>
					</div>
					<p >contenu</p>
				</div>
			</div>
		</article>
	)
}