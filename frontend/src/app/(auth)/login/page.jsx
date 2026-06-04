import Image from "next/image"
import styles from "../../../styles/login.module.css"

export default function Home() {
	return (
		<div className={styles.container}>
			<div className={styles.login}>
				<Image
					className={styles.logo}
					src="/IMGAppli/logo.png"
					alt="NewsFoundry Logo"
					width={195}
					height={17} />
				<p className={styles.text}>Connectez-vous pour accéder à votre assistant d'actualités IA</p>
				<form className={styles.form}>
					<label htmlFor="email">Adresse email</label>
					<input className={styles.input} type="email" placeholder="votre.email@exemple.com" />
					<button className={styles.btn}>Se connecter</button>
				</form>
			</div>
		</div>
	)
}