import * as Dialog from "@radix-ui/react-dialog";
import styles from "../../styles/modal.module.css"

export default function Modal({openModal, setOpenModal}) {
	return (
		<>
			<Dialog.Root open={openModal}
	onOpenChange={setOpenModal}>
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
						<form>
						{/* <form onSubmit={handleSubmit}> */}
							<div className={styles.field}>
								<label className={styles.label} htmlFor="title">Thème de la revue de presse</label>
								<input
									className={styles.input}
									id="title"
									type="text"
									// value={title}
									// onChange={(e) => setTitle(e.target.value)}

								/>
							</div>
							<button className={styles.btn}>Générer</button>
						</form>
						<Dialog.Close asChild />
					</Dialog.Content>
				</Dialog.Portal>
			</Dialog.Root>
		</>
	)
}