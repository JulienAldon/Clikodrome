import styles from './style.module.css';
import { useState } from 'preact/hooks';
import useAuthGuard from '../../context/useUser';
import useSessions from '../../hooks/useSessions';
import useSessionStatus from '../../hooks/useSessionStatus';
import Button from '../../components/button';
import { route } from 'preact-router';
import { createSession, removeSession } from '../../api';
import { useToast } from '../../context/toast';
import { useTranslation } from 'react-i18next';
import SessionsTable from '../../components/sessionsTable';
import useCityFilter from '../../hooks/useCityFilter';
import ComboBox from '../../components/combobox';

export default function Home() {
    const { token, intraRole } = useAuthGuard(undefined);
	const { sessions, fetchSessions } = useSessions();
    const { toastList, setToastList } = useToast();
	const { sessionStatus, fetchSessionStatus } = useSessionStatus();
	const [ loadingMorning, setLoadingMorning ] = useState(false);
	const [ loadingEvening, setLoadingEvening ] = useState(false);
	const [ loadingSessionList, setLoadingSessionList ] = useState([]);
	const { t, i18n } = useTranslation();

	const {
        filteredList: sessionShow,
        cityFilter: cityFilter,
        setCityFilter: setCityFilter, 
        handleCityFilterChange: handleCityFilterChange,
        cities: cities
    } = useCityFilter({sourceList:sessions});

	return (
		<>
			<section class={`page-body ${styles.home}`}>
			{
                cities ?
                <ComboBox 
                    class={styles.managerInputCombo}
                    title={t("Filter by city")}
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
			{
				sessionStatus ? <main class={styles.main}>
						<h2>{t('Create session')}</h2>
						<Button 
							deactivated={sessionStatus.morning ? true : false}
							description={t('Create morning session')}
							title={t("Morning")}
							loading={loadingMorning}
							action={() => {
							setLoadingMorning(true);
							createSession(token, '0').then((res) => {
								setLoadingMorning(false);
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
										description: t("Morning clicodrome session created."),
										backgroundColor: "rgba(15, 150, 150)",
									}]});
								}
							})
						}}></Button>
						<Button 
							deactivated={sessionStatus.evening ? true : false}
							description={t("Create evening session")}
							title={t('Evening')} 
							loading={loadingEvening}
							action={() => {
							setLoadingEvening(true);
							createSession(token, '-1').then((res) => {
								setLoadingEvening(false);
								if (res.detail && res.detail==="No edusign session available") {
									setToastList((toastList) => {return [...toastList, {
										id: 'createSession',
										title: t("Error"),
										description: t("No clicodrome session can be created today (no edusign session available)."),
										backgroundColor: "rgba(150, 15, 15)",
									}]});
								} else if (res.detail && res.detail==="Session already created") {
									setToastList((toastList) => {return [...toastList, {
										id: 'createSession',
										title: t("Error"),
										description: t("Session already created for this date and hour"),
										backgroundColor: "rgba(150, 15, 15)",
									}]});
								} else {
									fetchSessions();
									fetchSessionStatus();
									setToastList((toastList) => {return [...toastList, {
										id: 'createSession',
										title: t("Information"),
										description: t("Evening clicodrome session created."),
										backgroundColor: "rgba(15, 150, 150)",
									}]});
								}
							})
						}}></Button>
					<h2>{t('All sessions')}</h2> 
				{/* {
					sessions ? 
					sessions.map((elem, index) => {
						return (
						<div class={styles.session}>
							<a href={`/session/${elem.id}`}>
								<span>Session #{elem.id}</span>
								<span>{elem.date}</span>
								<span>{elem.hour.slice(0, 8)}</span>
							</a>
							<Button
								title=""
								deactivated={false}
								description={t("Delete the session")}
								loading={loadingSessionList[index]}
								action={() => {
									const loadingTmp = [
										...loadingSessionList.slice(0, index),
										true,
										...loadingSessionList.slice(index + 1)
									];
									setLoadingSessionList(loadingTmp);
									loadingSessionList[index] = true;
									removeSession(token, elem.id).then((res) => {
										setToastList((toastList) => {return [...toastList, {
											id: 'deleteSession',
											title: t('Information'),
											description: t("Session deleted successfully."),
											backgroundColor: "rgba(15, 150, 150)",
										}]});
										const loadingTmp = [
											...loadingSessionList.slice(0, index),
											false, 
											...loadingSessionList.slice(index + 1)
										];
										setLoadingSessionList(loadingTmp);
										fetchSessions();
										fetchSessionStatus();
									})
								}}
							></Button>
						</div>
						);
					}) : null
				} */}
				{	sessionShow ? 
					<SessionsTable
						onClickRow={(id)=>{
							route("/session/"+id);
						}}
						sessionList={sessionShow}
						sessionHead={[
							{name: "Action", id: "action", stateIcon: ""},
							{name: "Id", id: "id", stateIcon: ">"},
							{name: "City", id: "city", stateIcon: ">"},
							{name: "Date", id: "date", stateIcon: ">"},
							{name: "Hour", id: "hour", stateIcon: ">"},
						]}
						defaultSort="id"
					/> : <p>{t('No sessions available')}</p>
            	}
				</main> : null
			}
			</section>
		</>
	);
}
