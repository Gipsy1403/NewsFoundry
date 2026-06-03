// const API_URL = process.env.NEXT_PUBLIC_API_URL;

// /**
//  * Fonction générique pour appeler le backend
//  */
// export async function fetchAPI(endpoint) {
// 	console.log("API_URL =", process.env.NEXT_PUBLIC_API_URL);
//   const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}${endpoint}`);

//   console.log("STATUS =", res.status); // 👈 AJOUT IMPORTANT

//   const text = await res.text();
//   console.log("RAW RESPONSE =", text); // 👈 très important

//   if (!res.ok) {
//     throw new Error("Erreur API");
//   }

//   return JSON.parse(text);
// }