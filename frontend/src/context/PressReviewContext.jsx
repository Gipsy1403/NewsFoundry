// Gestionnaire des revues de presse côté frontend
// Partage les données entre plusieurs composants sans devoir passer des props partout
"use client";

import { createContext, useContext, useEffect, useState } from "react";
import {getPressReviews,createPressReview as apiCreatePressReview,} from "@/lib/api/pressReviewService";

// création du contexte
const PressReviewContext = createContext();

export function PressReviewProvider({ children }) {
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(false);
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState("");

//   charge toutes les revues de presse depuis l'API
  async function loadReviews() {
    try {
      setError("");
      setLoading(true);
      const data = await getPressReviews();
      setReviews(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error(err);
      setError("Impossible de charger les revues de presse.");
      setReviews([]);
    } finally {
      setLoading(false);
    }
  }

//   crée une nouvelle revue de presse puis l'ajoute au début de la liste
  async function createPressReview(chatId, subject) {
    if (!chatId || !subject?.trim()) {
      setError("Le sujet de la revue est requis.");
      return null;
    }
    try {
      setError("");
      setCreating(true);
      const newReview = await apiCreatePressReview(chatId, subject);
      setReviews((prev) => [newReview, ...prev]);
      return newReview;
    } catch (err) {
      console.error(err);
      setError("Impossible de créer la revue de presse.");
      return null;
    } finally {
      setCreating(false);
    }
  }

// Chargement des revues de presse au premier affichage du composant
  useEffect(() => {
    async function initPressReview() {
	await loadReviews();
    }
    initPressReview();
  }, []);

  return (
    <PressReviewContext.Provider
      value={{ reviews, loading, creating, error, loadReviews, createPressReview }}
    >
      {children}
    </PressReviewContext.Provider>
  );
}

export function usePressReview() {
  return useContext(PressReviewContext);
}
