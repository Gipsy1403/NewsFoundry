import HeaderDynamic from "../components/Headers/HeaderDynamic";
import SideBar from "../components/SideBar";
import Footer from "../components/Footer";
import styles from "../layout.module.css";
import { ChatProvider } from "@/context/ChatContext";
import { PressReviewProvider } from "@/context/PressReviewContext";

export default function PagesLayout({ children}) {
  return (
	<ChatProvider>
		<PressReviewProvider>
			<div className={styles.container}>
				<HeaderDynamic />
				<div className={styles.content}>
					<SideBar />
					<main className={styles.main}>
						{children}
					</main>
				</div>
				<Footer/>
			</div>
		</PressReviewProvider>
	</ChatProvider>
  );
}