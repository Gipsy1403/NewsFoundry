import styles from "@/styles/home.module.css";
import Image from "next/image";

export default function Home() {
	return (
		<>
			<div className={styles.main}>
				<div className={styles.content}>
														<Image
						className={styles.robot}
						src="/IMGAppli/animationRobot.png"
						alt="Robot IA animé"
						width={82}
						height={67} />
					<h1>Assistant Revue de Press IA</h1>
					<p className={styles.assistantText}>Posez-moi des questions sur l'actualité récente ou demandez-moi de générer une revue de presse sur un sujet spécifique.</p>
					<div className={styles.examples}>
						<p className={styles.examplesTitle}>Exemples :</p>
						<ul className={styles.examplesList}>
							<li>"Quelles sont les dernières nouvelles en politique ?"</li>
							<li>"Génère une revue de presse sur la technologie"</li>
							<li>"Résume l'actualité économique de la semaine"</li>
						</ul>
					</div>
				</div>
			</div>
		</>
	)
}