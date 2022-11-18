import { useState, useEffect } from 'preact/hooks';
import Button from '../../components/button';
import StudentEntry from '../../components/studentEntry';
import { getSession, validateSession, modifySession, signSession} from '../../api';
import styles from './style.module.css';
import useAuthGuard from '../../context/useUser';
import SearchBar from '../../components/searchBar';
import { useToast } from '../../context/toast';
import useSession from '../../hooks/useSession';

function addZero(i) {
    if (i < 10) {
        i = "0" + i
    }
    return i;
}

export default function Session(props) {
    const [searchStudent, setSearchStudent] = useState(undefined)
    const token = useAuthGuard()
    const { toastList, setToastList } = useToast();
    const { students, session, fetchSession } = useSession(props.id);

    const handleChange = (login) => {
        if (!students)
            return;
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
                    title: "Info",
                    description: "Students status has been saved.",
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
                    title: "Info",
                    description: "Students status has been saved.",
                    backgroundColor: "rgba(15, 150, 150)",
                }]});
            fetchSession();
        });
    }

    const handleSearchChange = (event) => {
        setSearchStudent(students.filter((el) => el.login.includes(event.target.value)));

    }

    return (
        <>
        {
            session ?
            <section>
                <div class={`${styles.center} ${styles.buttonBox}`}>
                    <Button deactivated={false} description="Allow session to be signed." title="Validate" action={() => {
                        validateSession(token, props.id).then((res) => {
                            modifySession(token, props.id, students).then((res) => {
                                setToastList((toastList) => {return [...toastList, {
                                    id: props.id,
                                    title: "Info",
                                    description: "Session has been validated, students status has been saved.",
                                    backgroundColor: "rgba(15, 150, 150)",
                                }]});
                            });
                        });
                    }}></Button>
                    <Button 
                        deactivated={session[0].is_approved === 1 ? false : true } 
                        description="Send all mails for the session." 
                        title="Send mail" 
                        action={() => {
                        modifySession(token, props.id, students).then((res) => {
                            signSession(token, props.id).then((res) => {
                                if (res.detail) {
                                    setToastList((toastList) => {return [...toastList, {
                                        id: props.id,
                                        title: "Error",
                                        description: "Session need validation by clicking on Validate.",
                                        backgroundColor: "rgba(150, 15, 15)",
                                    }]});
                                } else {
                                    setToastList((toastList) => {return [...toastList, {
                                        id: props.id,
                                        title: "Info",
                                        description: "All emails have been sent, students status has been saved.",
                                        backgroundColor: "rgba(15, 150, 150)",
                                    }]});
                                }
                            })
                        })
                        }}>
                    </Button>
                    <Button deactivated={false} description="Destroy and recreate session, fetching all students an other time." title="Refresh Session" action={() => {
                        setToastList((toastList) => {return [...toastList, {
                            id: props.id,
                            title: "Info",
                            description: "Not yet implemented.",
                            backgroundColor: "rgba(150, 15, 15)",
                        }]});
                        // TODO: implement refresh session button
                    }}></Button>
                </div>
                <div class={`${styles.center}`}>
                    <SearchBar 
                    placeholder="Search Student" 
                    description="Search student" 
                    onChange={handleSearchChange} 
                    onClear={() => {setSearchStudent(students)}}></SearchBar>
                </div>
                <table class={styles.centerCol}>
                    <tr class={styles.box}>
                        <th class={styles.label}>login</th>
                        <th class={styles.padding}>Present</th>
                        <th>Late</th>
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