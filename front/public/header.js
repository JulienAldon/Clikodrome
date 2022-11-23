import settings from './settings';
import {useAuth} from './context/auth'
import { logout } from './context/useUser'

export default function Header() {
	const token = useAuth()

	function login() {
		window.location.replace(`${settings.SERVICE_URL}/auth/azure`)
	}

	return (
		<header>
			<nav>
				<a class="home" href="/"></a>
				<a href="/sessions">Sessions</a>
				<a href="/remote">Distanciel</a>
			</nav>
			<label>
			{
				token ? <button class="button" onClick={logout}>Logout</button> :
				<button class="button" onClick={login}>Login</button>
			}
			</label>
		</header>
	);
}