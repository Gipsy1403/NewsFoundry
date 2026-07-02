import Link from "next/link";
import Image from "next/image";
import styles from "../styles/not-found.module.css";

export default function NotFound() {
	return (
		<main id="main-content" className={styles.container}>
			
			{/* Image principale */}
			<Image
				src="/IMGAppli/logo.png"
				alt="NewsFoundry Logo"
				width={148}
				height={15}
				priority
			/>

			{/* Image animée */}
			<div className={styles.robotContainer}>
				<Image
					src="/IMGAppli/animationRobot.png"
					alt="Robot IA animé"
					width={82}
					height={67}
				/>
			</div>

			<h1 className={styles.title}>404</h1>

			<h2 className={styles.subtitle}>
			Oups, cette page n'existe pas
			</h2>

			<p className={styles.description}>
			La page que vous recherchez a peut-être été déplacée,
			supprimée ou l'adresse saisie est incorrecte.
			</p>

			<Link href="/home" className={styles.button}>
			Retour à l'accueil
			</Link>

		</main>
	);
}