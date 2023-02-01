import styles from './style.module.css';
import { login } from '../../context/useUser';
import { useAuth } from '../../context/auth';
import Volet from '../../components/volet';
import { useTranslation } from 'react-i18next';

export default function About() {
	const token = useAuth()
	const { t, i18n } = useTranslation();

	return (
		<section class={`page-body ${styles.about} ${token ? "" : styles.disconnected}`}>
			<h1>{t('Welcome to Clicodrome')}</h1>
			<h2>{t('Cohesive Listing Initiative Concerning Official Date Recollection Over Mediocre Edusign')}</h2>
			{
				token ?
				<div class={`${styles.divLink}`}>
					<Volet title={t("Why clicodrome ?")}>
					<p>
						Clicodrome is part of our attendance process in Lyon. Its function is to automate the sending of <b>presence emails</b>.<br/>
						We use an <a href="https://intra.epitech.eu/module/2021/W-ADM-007/LYN-0-1/acti-505014"><b>activity</b></a> on the intranet to store sessions two times a day (9:00am-9:30am and 5:00pm-5:30pm).
						To planify all the sessions on the epitech intranet we use a <a href="https://github.com/JulienAldon/EEPlanner"><b>script</b></a>. <br/>
						We use <b>e-token</b> (phone application) to scan students cards updating previously planified intranet sessions with student status. <br/>
						The purpose of Clicodrome is to retrieve <b>intranet session</b> presence status, add potential late status ant then send all <b>presence emails</b> on edusign.
					</p>
					</Volet>
					<Volet title={t("How to use the clicodrome ?")}>
					<ul>
						<li>Create <b>clicodrome session</b> when sign session has ended (Example: In Lyon its at 9:30 for morning and 17:30 for evening) this will retrieve all presence status from the intranet.</li>
						<li>Once <b>clicodrome session</b> is created you can access it under "Sessions" tab and see which student is present or not (sliders represent if a student is present).</li>
						<li>You can set a student late by clicking on the late slider: this will automatically save the hour of delay.</li>
						<li>Validate the <b>clicodrome session</b> when everything is finished by clicking on "Validate" button.</li>
						<li>Finaly click on "Send email" button to send the edusign <b>presence emails</b> to students.</li>
						<li>You can add authorized remote under the tab "remote" by specifying a start date and end date and the student login, <b>presence emails</b> will be sent automatically for them.</li>
					</ul>
					</Volet>
					<Volet title={t("What clicodrome do ?")}>
						<ul>
							<li>Retrieve from epitech intranet presence status for a given session.</li>
							<li>Set / Unset presence status.</li>
							<li>Set late status saving the delay automatically.</li>
							<li>Send edusign <b>presence emails</b> for students marked as "present"</li>
						</ul>
					</Volet>
					<Volet title={t("What clicodrome doesn't do ?")}>
					<ul>
						<li>Set early departure in edusign (feel free to make a PR with the functionnality).</li>
						<li>Justified absences are not supported, you still need to upload manually for each edusign session. (this might be a future feature)</li>
					</ul>
					</Volet>
				</div>
				:
				<button class="button" onClick={login}>Login with office 365</button>
			}
		</section>
	);
}