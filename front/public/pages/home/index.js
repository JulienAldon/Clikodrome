import styles from './style.module.css';
import { login } from '../../context/useUser';
import { useAuth } from '../../context/auth';
import Volet from '../../components/volet';

export default function About() {
	const token = useAuth()
	return (
		<section class={`${styles.about} ${token ? "" : styles.disconnected}`}>
			<h1>Welcome to Clikodrome</h1>
			{
				token ?
				<div class={`${styles.divLink}`}>
					<Volet title="Why clikodrome ?">
					<p>
						Clikodrome is part of our attendance process in Lyon. Its function is to automate the sending of <b>presence emails</b>.<br/>
						We use an <a href="https://intra.epitech.eu/module/2021/W-ADM-007/LYN-0-1/acti-505014"><b>activity</b></a> on the intranet to store sessions two times a day (9:00am-9:30am and 5:00pm-5:30pm).
						To planify all the sessions on the epitech intranet we use a <a href="https://github.com/JulienAldon/EEPlanner"><b>script</b></a>. <br/>
						We use <b>e-token</b> (phone application) to validate presences inside previously planified intranet sessions. <br/>
						The purpose of Clikodrome is to retrieve <b>intranet session</b> presence status, add potential late status ant then send all emails on edusign.
					</p>
					</Volet>
					<Volet title="How to use the clikodrome ?">
					<ul>
						<li>Create session when physical sign session has ended (Example: In Lyon its at 9:30 for morning and 17:30 for evening) this will retrieve all presence status on the intranet.</li>
						<li>Once session is created you can access it and see which student is present or not (sliders represent if a student is present or not).</li>
						<li>You can set a student late by clicking on the late slider: this will automatically save the hour of delay.</li>
						<li>Validate the clikodrome session when everything is finished by clicking on "Validate" button.</li>
						<li>Finaly click on "Send mail" button to send the edusign presence emails to students.</li>
						<li>You can add authorized remote under the tab "remote" by specifying a start date and end date and the student login, presence emails will be sent automatically for them.</li>
					</ul>
					</Volet>
					<Volet title="What clikodrome do ?">
						<ul>
							<li>Get from epitech intranet presence status for each registered student.</li>
							<li>Set presence status for students.</li>
							<li>Set late status for student.</li>
							<li>Send automatically edusign emails to students..</li>
						</ul>
					</Volet>
					<Volet title="What clikodrome doesn't do ?">
					<ul>
						<li>Set early departure in edusign (feel free to make a PR with the functionnality).</li>
						<li>Justified absences are not supported, you still need to upload manually for each edusign session.</li>
					</ul>
					</Volet>
					<a class={`${styles.link}`} href="/sessions">Sessions</a>
					<a class={`${styles.link}`} href="/remote">Remote</a>
				</div>
				:
				<button class="button" onClick={login}>Login with office 365</button>
			}
		</section>
	);
}

