"use client";
import styles from "./page.module.css";
import { useEffect, useState } from "react";
import { fetchAPI } from "./lib/api";

export default function Home() {
  const [data, setData] = useState(null);

  useEffect(() => {
    async function loadData() {
      try {
        const result = await fetchAPI("/hello");
	   console.log("RESULT API =", result);
        setData(result);
      } catch (err) {
        console.error(err);
      }
    }

    loadData();
  }, []);

  return (
    <div>
      <h1>NewsFoundry</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}