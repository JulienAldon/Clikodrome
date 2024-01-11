import styles from './style.module.css';
import { useState } from 'preact/hooks';
import useAuthGuard from '../../context/useUser';
import useSessions from '../../hooks/useSessions';
import useSessionStatus from '../../hooks/useSessionStatus';
import { createSession, removeSession } from '../../api';
import { useToast } from '../../context/toast';
import { useTranslation } from 'react-i18next';
import SessionsTable from '../../components/sessionsTable';
import useCityFilter from '../../hooks/useCityFilter';
import ComboBox from '../../components/combobox';
import useFormInput from '../../hooks/useFormInput';
import SessionCreationPanel from '../../components/sessionCreationPanel';

export default function Home() {
    const { token, intraRole } = useAuthGuard(undefined);
	const { sessions, fetchSessions } = useSessions();
    const { toastList, setToastList } = useToast();
	const { sessionStatus, fetchSessionStatus } = useSessionStatus();
	const [ loadingSession, setLoadingSession ] = useState(false);
	const [ loadingSessionList, setLoadingSessionList ] = useState([]);
	const { t, i18n } = useTranslation();
	const [ showCreationPanel, setshowCreationPanel ] = useState(false);

	const periodProps = useFormInput();
	const cityProps = useFormInput();
    const dateProps = useFormInput();

	const {
        filteredList: sessionShow,
        cityFilter: cityFilter,
        setCityFilter: setCityFilter, 
        handleCityFilterChange: handleCityFilterChange,
        cities: cities
    } = useCityFilter({sourceList:sessions});

	const handleCreateSession = () => {
		if (periodProps.value === "" || periodProps.value === null || 
			dateProps.value === "" || dateProps.value === null || 
			cityProps.value === "" || cityProps.value === null) {
			setToastList((toastList) => {return [...toastList, {
				id: 'createSession',
				title: t("Error"),
				description: t("Cannot create promotion, missing field, please provide, date, period and city"),
				backgroundColor: "rgba(150, 15, 15)",
			}]});
			return;
		}
		setLoadingSession(true);
		let period = periodProps.value === 'Morning' ? '0' : '-1';
		createSession(token, period, dateProps.value, cityProps.value).then((res) => {
			setLoadingSession(false);
			if (res.detail && res.detail==="No edusign session available") {
				setToastList((toastList) => {return [...toastList, {
					id: 'createSession',
					title: t("Error"),
					description: t("No clicodrome session can be created today : no edusign session available."),
					backgroundColor: "rgba(150, 15, 15)",
				}]});
			} else {
				fetchSessions();
				fetchSessionStatus();
				setToastList((toastList) => {return [...toastList, {
					id: 'createSession',
					title: t("Information"),
					description: t("Clicodrome session created."),
					backgroundColor: "rgba(15, 150, 150)",
				}]});
			}
		})
	}

	const setElementInLoadingList = (index, value, setter, custom_list) => {
        const loadingTmp = [
            ...custom_list.slice(0, index),
            value, 
            ...custom_list.slice(index + 1)
        ];
        setter(loadingTmp);
    }

	const handleDeleteSession = (index, event) => {
        if (!event.target.value) {
            return;
        }
        setElementInLoadingList(index, true, setLoadingSessionList, loadingSessionList);
        removeSession(token, event.target.value).then((e) => {
            setToastList((toastList) => {return [...toastList, {
                id: 1,
                title: t("Information"),
                description: `${t('t("Session deleted successfully.")')}`,
                backgroundColor: "rgba(15, 150, 150)",
            }]});
            fetchSessions();
			setElementInLoadingList(index, false, setLoadingSessionList, loadingSessionList);
        })
    }

	return (
		<>
			<section class={`${styles.pageBody} ${styles.home}`}>
			{
				sessionStatus ? <main class={styles.main}>
				<h2
					className={styles.showTitle}
					onClick={() => setshowCreationPanel(!showCreationPanel)}
				>{t('Create session')}</h2>				
				{
					<SessionCreationPanel
						cities={cities}
						cityProps={cityProps}
						periodProps={periodProps}
						dateProps={dateProps}
						loadingSession={loadingSession}
						handleCreateSession={handleCreateSession}
						show={showCreationPanel}
					/>
				}
				<h2>{t('All sessions')}</h2>
				{
					cities ?
					<ComboBox 
						class={styles.sessionInputCombo}
						title={t("Enter city")}
						onChange={handleCityFilterChange}
						handleClear={() => {
							setCityFilter("");
						}}
						datalist_id={"city_list"}>
						{
							cities.map((el) => {
								return <option id={el} value={el}>{el}</option>
							})
						}
					</ComboBox> : null
				}
				{	sessionShow ? 
					<SessionsTable
						sessionList={sessionShow}
						sessionHead={[
							{name: "Id", id: "id", stateIcon: ">"},
							{name: "City", id: "city", stateIcon: ">"},
							{name: "Date", id: "date", stateIcon: ">"},
							{name: "Hour", id: "hour", stateIcon: ">"},
						]}
						defaultSort="id"
						loadingList={loadingSessionList}
						handleDeleteElement={handleDeleteSession}
					/> : <p>{t('No sessions available')}</p>
            	}
				</main> : null
			}
			</section>
		</>
	);
}