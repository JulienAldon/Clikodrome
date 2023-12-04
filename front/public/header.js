import settings from './settings';
import {useAuth} from './context/auth'
import { logout, login } from './context/useUser'
import { useTranslation } from 'react-i18next';
import { useEffect } from 'preact/hooks';

export default function Header() {
	const {token, intraRole} = useAuth()
	const { t, i18n } = useTranslation();

	return (
		<header class="page-header">
			<nav>
				<a class="home" href="/"></a>
				<a href="/sessions">{t('Sessions')}</a>
				{ intraRole === "pedago" ? <a href="/remote">{t('Remote')}</a> : null}
				{ intraRole === "pedago" ? <a href="/manager">{t('Manager')}</a> : null}	
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