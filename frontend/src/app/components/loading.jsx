// components/LoadingMessage.jsx

"use client";

import * as Progress from "@radix-ui/react-progress";
import styles from "../../styles/loading.module.css";

export default function Loading() {
	return (
		<div className={styles.container}>
			<Progress.Root
				className={styles.ProgressRoot}
				value={100}
			>
				<Progress.Indicator
					className={styles.ProgressIndicator}
				/>
			</Progress.Root>
		</div>
	);
}