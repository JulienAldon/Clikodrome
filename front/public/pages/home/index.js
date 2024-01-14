import styles from './style.module.css';
import { login } from '../../context/useUser';
import { useAuth } from '../../context/auth';
import Volet from '../../components/volet';
import { useTranslation } from 'react-i18next';
import Button from '../../components/button';

export default function About() {
    const { token, intraRole} = useAuth()
	const { t, i18n } = useTranslation();

	return (
		<section class={`page-body ${styles.about} ${token ? "" : styles.disconnected}`}>
			<h1>{t('Welcome to Clicodrome')}</h1>
			{
				token ?
				<div class={`${styles.divLink}`}>
					<Volet title={t("Why clicodrome ?")}>
					<p>
						Clicodrome is a tool designed to manage attendance sheets. It is linked with a sign provider, for now edusign.
						We use this solution to have a more practical UI for attendance sheet manipulation. It is linked to clicoscan desktop software to scan NFC cards.
					</p>
					</Volet>
					<Volet title={t("How to use the clicodrome ?")}>
					<ul>
					</ul>
					</Volet>
					<Volet title={t("What clicodrome do ?")}>
						<ul>
						</ul>
					</Volet>
					<Volet title={t("What clicodrome doesn't do ?")}>
					<ul>
					</ul>
					</Volet>
				</div>
				:
				<Button
					action={login}
					title={t("Login with office 365")}
					description={t("Login with office 365")}
				/>
			}
		</section>
	);
}