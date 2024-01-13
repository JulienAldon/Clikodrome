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
import FetchButton from '../../components/fetchButton';
import SignaturePanel from '../../components/signaturePanel';

export default function Session(props) {
    const { students, session, fetchSession, setStudents, signLinks, fetchSignatureLink, signatureLinkLoader } = useSession(props.id);
    const [ displayStudents, setDisplayStudents ] = useState([]);
    const [ currentSearch, setCurrentSearch ] = useState("");

    const { token, intraRole } = useAuthGuard(undefined);
    
    const [ toggleSortPresent, setToggleSortPresent ] = useState(undefined);
    const [ toggleSortLogin, setToggleSortLogin ] = useState(true);
    
    const [ signLoading, setSignLoading ] = useState(false);
    const [ validationLoading, setValidationLoading ] = useState(false);
    const [ refreshLoading, setRefreshLoading ] = useState(false);
    
    const { toastList, setToastList } = useToast();
	const { t, i18n } = useTranslation();
	const [ showSignaturePanel, setShowSignaturePanel ] = useState(false);

    const handleSearchChange = (event) => {
        setDisplayStudents(students.filter((el) => el.login.includes(event.target.value)));
        setCurrentSearch(event.target.value);
    }

    const setStudentStatus = (login) => {
        const s = students.map((stud) => {
            if (stud.login === login) {
                stud.status = stud.status === "present" ? "absent" : "present";
                return stud;
            }
            return stud;
        });
        setStudents([...s]);
    }

    const handleChange = (login) => {
        if (!students)
            return;
        setStudentStatus(login);
        const added_stud = students.filter(el => el.login === login);
        modifySession(token, props.id, added_stud).then((res) => {
            if (!res.detail) {
                setToastList((toastList) => {return [...toastList, {
                    id: props.id,
                    title: t("Information"),
                    description: t("Students status has been saved.") + " " + added_stud[0].login,
                    backgroundColor: "rgba(15, 150, 150)",
                }]});
            } else {
                setStudentStatus(login);
            }
        });
    }

    const fetchFromIntra = (id, activity) => {
        setRefreshLoading(true);
        refreshSession(token, id, activity).then((res) => {
            setRefreshLoading(false);
            if (res.detail) {
                setToastList((toastList) => {return [...toastList, {
                    id: id,
                    title: t("Information"),
                    description: t("Session could not be refreshed"),
                    backgroundColor: "rgba(150, 15, 15)",
                }]});
            } else {
                setToastList((toastList) => {return [...toastList, {
                    id: id,
                    title: t("Information"),
                    description: t("Session correctly refreshed."),
                    backgroundColor: "rgba(15, 150, 150)",
                }]});
            }
        })
    }

    const sortPresent = () => {
        setToggleSortPresent(!toggleSortPresent);
        setToggleSortLogin(undefined);
        const sortedStudents = [...students].sort((a, b) => {
            if (a.status === null || a.status === 'absent' || a.status === "NULL") {
                return toggleSortPresent ? -1 : 1;
            }
            if (a.status !== null || a.status !== 'absent' || a.status === "NULL") {
                return toggleSortPresent ? 1 : -1;
            }
            return 0
        });
        setStudents([...sortedStudents]);
    }

    const sortLogin = () => {
        setToggleSortPresent(undefined);
        setToggleSortLogin(!toggleSortLogin);
        const sortedStudents = [...students].sort((a, b) => {
            if (a.login < b.login) {
                return toggleSortLogin ? 1 : -1;
            }
            if (a.login > b.login) {
                return toggleSortLogin ? -1 : 1;
            }
            return 0
        });
        setStudents([...sortedStudents]);
    }

    useEffect(() => {
        if (students) {
            setDisplayStudents(students.filter((el) => el.login.includes(currentSearch)));
        }
    }, [students]);

    useEffect(() => {
        if (students) {
            setDisplayStudents(students.filter((el) => el.login.includes(currentSearch)));
        }
    }, [currentSearch])

    return (
        <>
        {
            session ?
            <section class="page-body">
                <div class={`${styles.sessionTitle}`}>
                    <h2>Session n°{session[0].id} {session[0].date} {session[0].hour.slice(0, 8)}</h2>
                </div>
                <h2
                    className={styles.signTitle}
                    onClick={() => {setShowSignaturePanel(!showSignaturePanel)}}
                >{t('Sign edusign sessions')}</h2>
                <SignaturePanel
                    signLinks={signLinks}
                    show={showSignaturePanel}
                    refetchSignList={fetchSignatureLink}
                    isRefetching={signatureLinkLoader}

                />
                {intraRole === "pedago" ? 
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
                    <FetchButton
                        refreshLoading={refreshLoading}
                        command={fetchFromIntra}
                        id={props.id}
                    />
                </div> : null}
                <div class={`${styles.center}`}>
                    <SearchBar 
                    placeholder={t("Search Student")} 
                    description={t("Search student")} 
                    onChange={handleSearchChange} 
                    onClear={() => {setCurrentSearch("")}}></SearchBar>
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
                    </tr>
                {
                    displayStudents ? <StudentEntry
                        students={displayStudents}
                        onChange={handleChange}
                       ></StudentEntry> : null
                }
                </table>
            </section> : null
        }
        </>
    )
}