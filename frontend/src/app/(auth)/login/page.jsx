"use client";

import Image from "next/image"
import styles from "../../../styles/login.module.css"
import { useState } from "react";
import { login } from "@/lib/api";
import { useRouter } from "next/navigation";

export default function Home() {
	const[email, setEmail]=useState("");
	const[password, setPassword]=useState("");
	const router=useRouter();

	async function handleLogin(e) {
		e.preventDefault();
		try {
console.log("EMAIL:", email);
console.log("PASSWORD:", password);
console.log("CALL LOGIN");
			// Appel API
			const data = await login(email,password);
console.log("RESPONSE", data)
			// Stockage JWT
			localStorage.setItem("token", data.access_token);

			router.push("/home")

			alert("Connexion réussie !");
		} catch (err) {
 console.error("LOGIN ERROR:", err);
			alert("Erreur de connexion");
		}
	}

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
				<form className={styles.form} onSubmit={handleLogin}>
					<label htmlFor="email">Adresse email</label>
					<input className={styles.input} type="email" placeholder="votre.email@exemple.com" onChange={(e) => setEmail(e.target.value)}/>
					<label htmlFor="password">Mot de passe</label>
					<input className={styles.input} placeholder="votre mot de passe" type="password" onChange={(e) => setPassword(e.target.value)}/>
					<button type="submit" className={styles.btn}>Se connecter</button>
				</form>
			</div>
		</div>
	)
}