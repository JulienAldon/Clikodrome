import styles from './style.module.css';
import { login } from '../../context/useUser';
import { useAuth } from '../../context/auth';

export default function About() {
	const token = useAuth()
	return (
		<section class={styles.about}>
			<h1>Welcome to Clikodrome</h1>
			{
				token ?
				<div class={`${styles.divLink}`}>
					<p>Go to sessions to start</p> 
					<a class={`${styles.link}`} href="/sessions">Sessions</a>
				</div>
				:
				<button class="button" onClick={login}>Login with office 365</button>
			}
		</section>
	);
}

