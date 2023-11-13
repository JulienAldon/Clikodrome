import { useState, useEffect } from 'preact/hooks';
import Button from '../../components/button';
import StudentEntry from '../../components/studentEntry';
import { refreshSession, validateSession, modifySession, signSession} from '../../api';
import styles from './style.module.css';
import useAuthGuard from '../../context/useUser';
import SearchBar from '../../components/searchBar';
import { useToast } from '../../context/toast';
import useSession from '../../hooks/useSession';
import { TableHead } from '../../components/tableHead';
import { useTranslation } from 'react-i18next';

function addZero(i) {
    if (i < 10) {
        i = "0" + i
    }
    return i;
}

export default function Session(props) {
    const [searchStudent, setSearchStudent] = useState(undefined);
    const token = useAuthGuard();
    const { toastList, setToastList } = useToast();
    const { students, session, fetchSession, setStudents } = useSession(props.id);
    const [ toggleSortPresent, setToggleSortPresent ] = useState(undefined);
    const [ toggleSortLate, setToggleSortLate ] = useState(undefined);
    const [ toggleSortLogin, setToggleSortLogin ] = useState(true);
    const [ signLoading, setSignLoading ] = useState(false);
    const [ validationLoading, setValidationLoading ] = useState(false);
    const [ refreshLoading, setRefreshLoading ] = useState(false);
	const { t, i18n } = useTranslation();

    const handleChange = (login) => {
        if (!students)
            return;
        console.log(students)
        students.forEach(element => {
            if (element.login === login) {
                if (element.late !== null && element.late !== 'NULL') {
                    element.late = 'NULL';
                    element.status = 'NULL';
                } else {
                    element.status = element.status === 'present' ? 'NULL' : 'present';
                }
            }
        });
        modifySession(token, props.id, students).then((res) => {
            if (!res.detail)
                setToastList((toastList) => {return [...toastList, {
                    id: props.id,
                    title: t("Information"),
                    description: t("Students status has been saved."),
                    backgroundColor: "rgba(15, 150, 150)",
                }]});
            fetchSession();
        });
    }

    const onLateChange = (login) => {
        if (!students)
            return;
        const date = new Date();
        students.forEach(element => {
            if (element.login === login) {
                let status = element.status != 'retard' ? 'retard' : 'NULL';
                let late = status === 'retard' ? `${addZero(date.getHours())}:${addZero(date.getMinutes())}:00` : 'NULL';
                element.status = status;
                element.late = late;
            }
        });
        modifySession(token, props.id, students).then((res) => {
            if (!res.detail)
                setToastList((toastList) => {return [...toastList, {
                    id: props.id,
                    title: t("Information"),
                    description: t("Students status has been saved."),
                    backgroundColor: "rgba(15, 150, 150)",
                }]});
            fetchSession();
        });
    }

    const handleSearchChange = (event) => {
        setSearchStudent(students.filter((el) => el.login.includes(event.target.value)));
    }

    const sortPresent = () => {
        setToggleSortPresent(!toggleSortPresent);
        setToggleSortLogin(undefined);
        setToggleSortLate(undefined);
        const sortedStudents = [...students].sort((a, b) => {
            if (a.status === null || a.status === 'NULL') {
                return toggleSortPresent ? -1 : 1;
            }
            if (a.status !== null || a.status !== 'NULL') {
                return toggleSortPresent ? 1 : -1;
            }
            return 0
        });
        setStudents(sortedStudents);
        if (searchStudent) {
            const sortedSearchStudents = [...searchStudent].sort((a, b) => {
                if (a.status === null || a.status === 'NULL') {
                    return toggleSortPresent ? -1 : 1;
                }
                if (a.status !== null || a.status !== 'NULL') {
                    return toggleSortPresent ? 1 : -1;
                }
                return 0
            });
            setSearchStudent(sortedSearchStudents);
        }
    }

    const sortLogin = () => {
        setToggleSortPresent(undefined);
        setToggleSortLogin(!toggleSortLogin);
        setToggleSortLate(undefined);
        const sortedStudents = [...students].sort((a, b) => {
            if (a.login < b.login) {
                return toggleSortLogin ? 1 : -1;
            }
            if (a.login > b.login) {
                return toggleSortLogin ? -1 : 1;
            }
            return 0
        });
        setStudents(sortedStudents);
        if (searchStudent) {
            const sortedSearchStudents = [...searchStudent].sort((a, b) => {
                if (a.login < b.login) {
                    return toggleSortLogin ? 1 : -1;
                }
                if (a.login > b.login) {
                    return toggleSortLogin ? -1 : 1;
                }
                return 0
            });
            setSearchStudent(sortedSearchStudents);
        }
    }

    const sortLate = () => {
        setToggleSortPresent(undefined);
        setToggleSortLate(!toggleSortLate);
        setToggleSortLogin(undefined);
        const sortedStudents = [...students].sort((a, b) => {
            if (a.late === null || a.late === 'NULL') {
                return toggleSortLate ? -1 : 1;
            }
            if (a.late !== null || a.late !== 'NULL') {
                return toggleSortLate ? 1 : -1;
            }
            return 0;
        });
        setStudents(sortedStudents);
        if (searchStudent) {
            const sortedSearchStudents = [...searchStudent].sort((a, b) => {
                if (a.late === null || a.late === 'NULL') {
                    return toggleSortLate ? -1 : 1;
                }
                if (a.late !== null || a.late !== 'NULL') {
                    return toggleSortLate ? 1 : -1;
                }
                return 0;
            });
            setSearchStudent(sortedSearchStudents);
        }
    }
    return (
        <>
        {
            session ?
            <section class="page-body">
                <div class={`${styles.sessionTitle}`}>
                    <h2>Session n°{session[0].id} {session[0].date} {session[0].hour.slice(0, 8)}</h2>
                </div>
                <div class={`${styles.center} ${styles.buttonBox}`}>
                    <Button 
                        deactivated={false} 
                        description={t("Allow session to be signed.")} 
                        title={t("Validate")} 
                        loading={validationLoading} 
                        action={() => {
                        setValidationLoading(true);
                        validateSession(token, props.id).then((res) => {
                            modifySession(token, props.id, students).then((res) => {
                                setValidationLoading(false);
                                setToastList((toastList) => {return [...toastList, {
                                    id: props.id,
                                    title: t("Information"),
                                    description: t("Session has been validated."),
                                    backgroundColor: "rgba(15, 150, 150)",
                                }]});
                                fetchSession();
                            });
                        });
                    }}>
                    </Button>
                    <Button 
                        deactivated={session[0].is_approved === 1 ? false : true } 
                        description={t("Send all emails for the session.")} 
                        title={t("Send emails")} 
                        loading={signLoading}
                        action={() => {
                        setSignLoading(true);
                        modifySession(token, props.id, students).then((res) => {
                            signSession(token, props.id).then((res) => {
                                setSignLoading(false);
                                if (res.detail) {
                                    setToastList((toastList) => {return [...toastList, {
                                        id: props.id,
                                        title: t("Error"),
                                        description: t("Session need validation by clicking on Validate."),
                                        backgroundColor: "rgba(150, 15, 15)",
                                    }]});
                                } else {
                                    setToastList((toastList) => {return [...toastList, {
                                        id: props.id,
                                        title: t("Information"),
                                        description: t("All emails have been sent."),
                                        backgroundColor: "rgba(15, 150, 150)",
                                    }]});
                                }
                            })
                        })
                        }}>
                    </Button>
                    <Button 
                        deactivated={false} 
                        description={t("Destroy and recreate session, fetching all students an other time.")} 
                        title={t("Refresh Session")} 
                        loading={refreshLoading}
                        action={() => {
                        setRefreshLoading(true);
                        refreshSession(token, props.id).then((res) => {
                            setRefreshLoading(false);
                            if (res.detail) {
                                setToastList((toastList) => {return [...toastList, {
                                    id: props.id,
                                    title: t("Information"),
                                    description: t("Session could not be refreshed"),
                                    backgroundColor: "rgba(150, 15, 15)",
                                }]});
                            } else {
                                setToastList((toastList) => {return [...toastList, {
                                    id: props.id,
                                    title: t("Information"),
                                    description: t("Session correctly refreshed."),
                                    backgroundColor: "rgba(15, 150, 150)",
                                }]});
                                fetchSession()
                            }
                        })
                    }}></Button>
                </div>
                <div class={`${styles.center}`}>
                    <SearchBar 
                    placeholder={t("Search Student")} 
                    description={t("Search student")} 
                    onChange={handleSearchChange} 
                    onClear={() => {setSearchStudent(students)}}></SearchBar>
                </div>
                <table class={styles.centerCol}>
                    <tr class={styles.box}>
                        <TableHead
                            title={t("Login")}
                            sortFunction={sortLogin}
                            toggleSort={toggleSortLogin}
                            addStyle={styles.label}
                        />
                        <TableHead
                            title={t("Present")}
                            sortFunction={sortPresent}
                            toggleSort={toggleSortPresent}
                            addStyle={styles.padding}
                        />
                        <TableHead
                            title={t("Late")}
                            sortFunction={sortLate}
                            toggleSort={toggleSortLate}
                        />
                    </tr>
                {
                    searchStudent ? (searchStudent ? <StudentEntry
                        students={searchStudent}
                        onChange={handleChange}
                        lateOnChange={onLateChange}
                       ></StudentEntry> : null) : (students ? <StudentEntry
                         students={students}
                         onChange={handleChange}
                         lateOnChange={onLateChange}
                        ></StudentEntry> : null) 
                }
                </table>
            </section> : null
        }
        </>
    )
}