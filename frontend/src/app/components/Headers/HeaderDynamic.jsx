"use client";

import { usePathname } from "next/navigation";
import Header1 from "./Header1";
import Header2 from "./Header2";


export default function HeaderDynamic() {
  const pathname = usePathname();
	if (pathname.startsWith("/chat")) {
		return <Header2 />;
	}
  return <Header1 />;
}