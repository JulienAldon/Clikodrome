import { useTranslation } from 'react-i18next';
import style from './style.module.css';

export default function Footer() {
	const { t, i18n } = useTranslation();
    const changeLanguage = (lng) => {
        i18n.changeLanguage(lng)
    }
    return (
        <footer class={`page-footer`}>
            <button class={`${i18n.language === 'en' ? style.selected : ""} ${style.langIcon}`} onClick={() => changeLanguage('en')}>
            <img src="https://img.icons8.com/fluency/48/null/great-britain-circular.png"/>
            </button>
            <button class={`${i18n.language === 'fr' ? style.selected : ""} ${style.langIcon}`} onClick={() => changeLanguage('fr')}>
            <img src="https://img.icons8.com/fluency/48/null/france-circular.png"/>
            </button>
        </footer>
    );
}