import settings from './settings';
import {useAuth, logout} from './context/auth'
import { login } from './context/useUser'
import { useTranslation } from 'react-i18next';
import { useEffect, useState } from 'preact/hooks';

export default function Header() {
	const {token, intraRole} = useAuth()
	const [argument, setArgument] = useState(undefined);
	const { t, i18n } = useTranslation();

	useEffect(() => {
	}, []);

	return (
		<header className="page-header">
			<nav>
				<a className="home" href="/"></a>
				{ token ? <a href={`/sessions${argument ? `/${argument}` : ''}`}>{t('Sessions')}</a> : null }
				{ intraRole === "pedago" ? <a href={`/remote${argument ? `/${argument}` : ''}`}>{t('Remote')}</a> : null}
				{ intraRole === "pedago" ? <a href={`/manager${argument ? `/${argument}` : ''}`}>{t('Manager')}</a> : null}	
			</nav>
			<label>
			{
				token ? <button className="button" onClick={logout}>{t('Logout')}</button> :
				<button className="button" onClick={login}>{t('Login')}</button>
			}
			</label>
		</header>
	);
}