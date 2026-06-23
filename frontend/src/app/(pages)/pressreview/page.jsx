"use client";

import { faCalendar} from "@fortawesome/free-regular-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import styles from "../../../styles/pressreview.module.css";
import { usePressReview } from "@/context/PressReviewContext";
import { useState } from "react";
import toast from "react-hot-toast";
import ReactMarkdown from "react-markdown";


export default function PressReview() {
	const { reviews, loading } = usePressReview();

	const [expandedId, setExpandedId] = useState(null);

	function formatDate(dateStr) {
		const date=new Date(`${dateStr}Z`);

	return date.toLocaleDateString("fr-FR", {
		weekday:"long",
		day: "numeric",
		month: "long",
		year: "numeric",
		hour:"2-digit",
		minute:"2-digit",
		timeZone:"Europe/Paris",
	});
	}

	function getWeekNumber(date) {
		const d = new Date(Date.UTC(
			date.getFullYear(),
			date.getMonth(),
			date.getDate()
		));

		// Lundi = début de semaine ISO
		const dayNum = d.getUTCDay() || 7;
		d.setUTCDate(d.getUTCDate() + 4 - dayNum);

		const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));

		return Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
	}

	function buildReviewTitle(subject, dateStr) {
		const date = new Date(dateStr);

		const weekNumber = getWeekNumber(date);
		const year = date.getFullYear();

		return `Actualités ${subject} - Semaine ${weekNumber}`;
	}

	function handleCopy(review) {
	const lines = [
		`${review.title}`,
		`${formatDate(review.created_at)}`,
		`Sujet : ${review.subject}`,
		``,
		review.markdown_content,
		``,
	];
	navigator.clipboard.writeText(lines.join("\n"));
	toast.success("Revue copiée dans le presse-papiers !");
	}

	if (loading) {
	return (
		<div className={styles.empty}>
		<p>Chargement...</p>
		</div>
	);
	}

	return (
		<article className={styles.containerPress}>
			<p className={styles.title}>Revues de Presse</p>
			<p className={styles.subTitle}>
			Consultez et gérez vos revues de presse générées par l'IA
			</p>

			<div className={styles.cardsContainer}>
			{reviews.map((review) => (
				<div className={styles.card} key={review.id}>
					
					{/* HEADER */}
					<div className={styles.headerCard}>
					<div>
						<p className={styles.titleCard}>{buildReviewTitle(
								review.subject,
								review.created_at
							)}</p>
						{/* <p className={styles.titleCard}>{review.title}</p> */}

						<div className={styles.dateCard}>
						<FontAwesomeIcon
						className={styles.iconCard}
						icon={faCalendar}
						/>
						{formatDate(review.created_at)}
						</div>
					</div>

					<button
						className={styles.btnCard}
						onClick={() => handleCopy(review)}
					>
						Copier
					</button>
					</div>

					{/* CONTENT MARKDOWN */}
					<div className={styles.markdown}>
						<ReactMarkdown>
							{review.markdown_content}
						</ReactMarkdown>
					</div>
				</div>
			))}
			</div>
		</article>


		// <article className={styles.containerPress} >
		// 	<p className={styles.title}>Revues de Presse</p>
		// 	<p className={styles.subTitle}>Consultez et gérez vos revues de presse générées par l'IA</p>
		// 	<div>
		// 		{reviews.map((review)=>{
		// 			const isOpen=expandedId ===review.id;
		// 			return (
		// 				<div className={styles.card} key={review.id}>
		// 					<div className={styles.headerCard}>
		// 						<div>
		// 							<p className={styles.titleCard}>{review.title}</p>
		// 							<div className={styles.dateCard}>
		// 								<FontAwesomeIcon className={styles.iconCard} icon={faCalendar} />{formatDate(review.created_at)}
		// 							</div>
		// 						</div>
		// 						<button className={styles.btnCard} onClick={()=>handleCopy(review)}>Copier</button>
		// 					</div>
		// 					{review.article_summaries?.length > 0 && (
		// 						<div className={styles.section}>
		// 							<p className={styles.sectionLabel}>Articles ({review.article_summaries.length})</p>
		// 							<div className={styles.articleList}>
		// 							{review.article_summaries.map((article, idx) => (
		// 								<div key={idx} className={styles.articleItem}>
		// 									<p className={styles.articleTitle}>{article.article_title}</p>
		// 									<p className={styles.articleSummary}>{article.summary}</p>
		// 								</div>
		// 							))}
		// 							</div>
		// 						</div>
		// 					)}
		// 						<ReactMarkdown>
		// 						{review.global_summary}
		// 						</ReactMarkdown>
		// 					{/* <div className={styles.article}>
		// 						<div className={styles.titleArticle}>
		// 							<p className={styles.titlePress}>revue de presse</p>
		// 							<p className={styles.datePress}>date</p>
		// 						</div>
		// 						<p >contenu</p>
		// 					</div> */}
		// 				</div>

		// 			)
		// 		})}

		// 	</div>
		// </article>
	)
}