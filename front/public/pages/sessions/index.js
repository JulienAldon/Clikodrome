import styles from './style.module.css';
import { useState } from 'preact/hooks';
import useAuthGuard from '../../context/useUser';
import useSessions from '../../hooks/useSessions';
import useSessionStatus from '../../hooks/useSessionStatus';
import { createSession, removeSession } from '../../api';
import { useToast } from '../../context/toast';
import { useTranslation } from 'react-i18next';
import TableDisplay from '../../components/tableDisplay';
import useCityFilter from '../../hooks/useCityFilter';
import ComboBox from '../../components/combobox';
import useFormInput from '../../hooks/useFormInput';
import SessionCreationPanel from '../../components/sessionCreationPanel';
import Volet from '../../components/volet';

export default function Sessions(props) {
    const { token, intraRole } = useAuthGuard(undefined);
	const { sessions, fetchSessions } = useSessions();
    const { toastList, setToastList } = useToast();
	const { sessionStatus, fetchSessionStatus } = useSessionStatus();
	const [ loadingSession, setLoadingSession ] = useState(false);
	const [ loadingSessionList, setLoadingSessionList ] = useState([]);
	const { t, i18n } = useTranslation();

	const periodProps = useFormInput();
	const cityProps = useFormInput();
    const dateProps = useFormInput();

	const {
        filteredList: sessionShow,
        cityFilter: cityFilter,
        setCityFilter: setCityFilter, 
        handleCityFilterChange: handleCityFilterChange,
        cities: cities
    } = useCityFilter({sourceList:sessions ? sessions : [], defaultValue:props.params.city !== undefined ? props.params.city : ""});

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
			if (res.detail) {
				setToastList((toastList) => {return [...toastList, {
					id: 'createSession',
					title: t("Error"),
					description: t(res.detail),
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
                description: `${t("Session deleted successfully.")}`,
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
				<Volet 
					className={styles.showTitle}
					title={t('Create session')}
				>
  					<SessionCreationPanel
						cities={cities}
						cityProps={cityProps}
						periodProps={periodProps}
						dateProps={dateProps}
						loadingSession={loadingSession}
						handleCreateSession={handleCreateSession}
					/>
				</Volet>
				<h2>{t('All sessions')}</h2>
				<div className={styles.filterSection}>
					{
						cities ?
						<ComboBox 
							class={styles.sessionInputCombo}
							title={t("Enter city")}
							value={cityFilter}
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
				</div>
				{	sessionShow ? 
					<TableDisplay
						tableList={sessionShow}
						tableHead={[
							{name: "Id", id: "id", stateIcon: ""},
							{name: "City", id: "city", stateIcon: ""},
							{name: "Date", id: "date", stateIcon: ""},
							{name: "Hour", id: "hour", stateIcon: ""},
						]}
						link={"/session/"}
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