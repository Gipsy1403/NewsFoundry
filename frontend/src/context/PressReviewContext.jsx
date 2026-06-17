// frontend/src/context/PressReviewContext.jsx
"use client";

import { createContext, useContext, useEffect, useState } from "react";
import {getPressReviews,createPressReview as apiCreatePressReview,} from "@/lib/api/pressReviewService";

const PressReviewContext = createContext();

export function PressReviewProvider({ children }) {
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(false);
  const [creating, setCreating] = useState(false);

  async function loadReviews() {
    try {
      setLoading(true);
      const data = await getPressReviews();
      setReviews(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error(err);
      setReviews([]);
    } finally {
      setLoading(false);
    }
  }

  async function createPressReview(chatId, subject) {
    if (!chatId || !subject?.trim()) return null;
    try {
      setCreating(true);
      const newReview = await apiCreatePressReview(chatId, subject);
      setReviews((prev) => [newReview, ...prev]);
      return newReview;
    } catch (err) {
      console.error(err);
      return null;
    } finally {
      setCreating(false);
    }
  }

  useEffect(() => {
    loadReviews();
  }, []);

  return (
    <PressReviewContext.Provider
      value={{ reviews, loading, creating, loadReviews, createPressReview }}
    >
      {children}
    </PressReviewContext.Provider>
  );
}

export function usePressReview() {
  return useContext(PressReviewContext);
}
