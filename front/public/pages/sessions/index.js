import styles from './style.module.css';
import useAuthGuard from '../../context/useUser';
import useSessions from '../../hooks/useSessions';
import useSessionStatus from '../../hooks/useSessionStatus';
import Button from '../../components/button';
import { createSession, removeSession } from '../../api';
import { useToast } from '../../context/toast';

export default function Home() {
	const token = useAuthGuard();
	const { sessions, fetchSessions } = useSessions();
    const { toastList, setToastList } = useToast();
	const { sessionStatus, fetchSessionStatus } = useSessionStatus();

	return (
		<>
			<section class={styles.home}>
			{
				sessionStatus ? <main class={styles.main}>
					<h2>Create session</h2>
					
					<Button 
						deactivated={sessionStatus.morning ? true : false}
						description="Create morning session" title="Matin" action={() => {
						createSession(token, '0').then((res) => {
							if (res.detail && res.detail==="No edusign session available") {
								setToastList((toastList) => {return [...toastList, {
									id: 'createSession',
									title: "Error",
									description: "No clicodrome session can be created today (no edusign session available).",
									backgroundColor: "rgba(150, 15, 15)",
								}]});
							} else {
								fetchSessions();
								fetchSessionStatus();
								setToastList((toastList) => {return [...toastList, {
									id: 'createSession',
									title: "Info",
									description: "Morning clicodrome session created.",
									backgroundColor: "rgba(15, 150, 150)",
								}]});
							}
						})
					}}></Button>
					<Button 
                    	deactivated={sessionStatus.evening ? true : false}
						description="Create evening session" title="Soir" action={() => {
						createSession(token, '-1').then((res) => {
							if (res.detail && res.detail==="No edusign session available") {
								setToastList((toastList) => {return [...toastList, {
									id: 'createSession',
									title: "Error",
									description: "No clicodrome session can be created today (no edusign session available).",
									backgroundColor: "rgba(150, 15, 15)",
								}]});
							} else if (res.detail && res.detail==="Session already created") {
								setToastList((toastList) => {return [...toastList, {
									id: 'createSession',
									title: "Error",
									description: "Session already created for this date and hour",
									backgroundColor: "rgba(150, 15, 15)",
								}]});
							} else {
								fetchSessions();
								fetchSessionStatus();
								setToastList((toastList) => {return [...toastList, {
									id: 'createSession',
									title: "Info",
									description: "Evening clicodrome session created.",
									backgroundColor: "rgba(15, 150, 150)",
								}]});
							}
						})
					}}></Button>

					<h2>All sessions</h2>
				{
					sessions ? 
					sessions.map((elem) => {
						return (
						<div class={styles.session}>
							<a href={`/session/${elem.id}`}>
								<span>Session #{elem.id}</span>
								<span>{elem.date}</span>
								<span>{elem.hour.slice(0, 8)}</span>
							</a>
							<Button
									title="???"
									deactivated={false}
									description="Delete the session"
									action={() => {
										removeSession(token, elem.id).then((res) => {
											setToastList((toastList) => {return [...toastList, {
												id: 'deleteSession',
												title: "Info",
												description: "Session deleted.",
												backgroundColor: "rgba(15, 150, 150)",
											}]});
											fetchSessions();
											fetchSessionStatus();
										})
									}}
								></Button>
						</div>
						);
					}) : null
				}
				</main> : null
			}
			</section>
		</>
	);
}
