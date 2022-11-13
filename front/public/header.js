import settings from './settings';
import {useAuth} from './context/auth'
import { logout } from './context/useUser'

export default function Header() {
	const token = useAuth()
	return (
		<header>
			<nav>
				<a href="/sessions">Sessions</a>
				<a href="/remote">Distanciel</a>
			</nav>
			<label>
			{
				token ? <button class="button" onClick={logout}>Logout</button> :
				<a class="button" href={`${settings.SERVICE_URL}/auth/azure`}>Login</a>
			}
			</label>
		</header>
	);
}