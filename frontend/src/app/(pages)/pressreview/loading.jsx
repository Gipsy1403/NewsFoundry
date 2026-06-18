import styles from "../../../styles/loading.module.css";


export default function Loading() {
	return (
    <div className={styles.overlay}>
      
      {/* Bloc centré */}
      <div className={styles.loaderBox}>

        {/* Spinner */}
        <div className={styles.spinner}></div>

        {/* Texte animé */}
        <div className={styles.textWrapper}>
          <p className={styles.text}>
            En cours de chargement...
          </p>
        </div>

      </div>
    </div>
	);
}