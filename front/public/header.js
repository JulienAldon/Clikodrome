import settings from './settings';
import {useAuth} from './context/auth'
import { logout } from './context/useUser'
import { useTranslation } from 'react-i18next';

export default function Header() {
	const token = useAuth()
	const { t, i18n } = useTranslation();

	function login() {
		window.location.replace(`${settings.SERVICE_URL}/auth/azure`)
	}

	return (
		<header class="page-header">
			<nav>
				<a class="home" href="/"></a>
				<a href="/sessions">{t('Sessions')}</a>
				<a href="/remote">{t('Remote')}</a>
			</nav>
			<label>
			{
				token ? <button class="button" onClick={logout}>{t('Logout')}</button> :
				<button class="button" onClick={login}>{t('Login')}</button>
			}
			</label>
		</header>
	);
}