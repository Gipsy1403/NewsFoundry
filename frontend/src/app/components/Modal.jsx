"use client";

import * as Dialog from "@radix-ui/react-dialog";
import styles from "../../styles/modal.module.css"
import { useState } from "react";
import { useChat } from "@/context/ChatContext";
import { usePressReview } from "@/context/PressReviewContext";
import { useRouter } from "next/navigation";
import toast from "react-hot-toast";

export default function Modal({openModal, setOpenModal}) {
	const [subject, setSubject] = useState("");
	const { chatId } = useChat();
	const { createPressReview, creating } = usePressReview();

	const router = useRouter();

	async function handleSubmit(e) {

		e.preventDefault();
		if (!subject.trim()) {
			toast.error("Veuillez saisir un thème.");
			return;
		}
		if (!chatId) {
			toast.error("Aucune conversation active.");
			return;
		}

		try {
			const review = await createPressReview(chatId, subject);

			if (!review) {
  				toast.error("La génération a échoué.");
				return;
			}

			toast.success("Revue de presse générée !");
			setOpenModal(false);
			setSubject("");
			router.push("/pressreview");

		} catch (error) {
			console.error(error);

			toast.error(
				error.message || "Erreur lors de la génération."
			);
		}
	}
	
	return (
		<>
			<Dialog.Root open={openModal} onOpenChange={setOpenModal}>
				<Dialog.Overlay className={styles.overlay}/>
				<Dialog.Portal>
					<Dialog.Content className={styles.content}>
						{/* <p className={styles.closeButton} aria-label="Fermer" onClick={() => setOpenModal(false)}>Fermer</p> */}
						<button className={styles.closeButton} onClick={() => setOpenModal(false)}>
							Fermer
						</button>
						<Dialog.Title className={styles.title}>Générer une revue de presse</Dialog.Title>
						{/* {error && <p styles={{ color: "red" }}>{error}</p>} */}
						<p className={styles.subTitle}>Donner un titre à votre revue de presse</p>
						<form onSubmit={handleSubmit}>
						{/* <form onSubmit={handleSubmit}> */}
							<div className={styles.field}>
								<label className={styles.label} htmlFor="subject">Thème de la revue de presse</label>
								<input
									className={styles.input}
									id="subject"
									type="text"
									placeholder="Ex : Intelligence artificielle, Économie..."
									value={subject}
									onChange={(e) => setSubject(e.target.value)}
									disabled={creating}

								/>
							</div>
							<button className={styles.btn} type="submit" disabled={creating}>
								{creating ? (
									<span className={styles.loadingContent}>
										<span className={styles.spinner}></span>
										Génération...
									</span>
								) : (
								"Générer"
								)}
							</button>
						</form>
						<Dialog.Close asChild />
					</Dialog.Content>
				</Dialog.Portal>
			</Dialog.Root>
		</>
	)
}