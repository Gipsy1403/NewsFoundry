"use client";

import { useState } from "react";
import HeaderDynamic from "../components/Headers/HeaderDynamic";
import SideBar from "../components/SideBar";
import Footer from "../components/Footer";
import styles from "../layout.module.css";
import { ChatProvider } from "@/context/ChatContext";
import { PressReviewProvider } from "@/context/PressReviewContext";

export default function PageShell({ children }) {
  const [drawerOpen, setDrawerOpen] = useState(false);
  const closeDrawer = () => setDrawerOpen(false);

  return (
    <ChatProvider>
      <PressReviewProvider>
        <div className={styles.container}>
          <HeaderDynamic drawerOpen={drawerOpen} setDrawerOpen={setDrawerOpen} />
          <div className={styles.content}>
            <SideBar drawerOpen={drawerOpen} setDrawerOpen={setDrawerOpen} />
            <main className={styles.main} onClick={closeDrawer} id="main-content">
              {children}
            </main>
          </div>
          <Footer />
        </div>
      </PressReviewProvider>
    </ChatProvider>
  );
}
