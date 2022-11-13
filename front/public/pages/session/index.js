import { useState, useEffect } from 'preact/hooks';
import Button from '../../components/button';
import StudentEntry from '../../components/studentEntry';
import { getSession, validateSession, modifySession, signSession} from '../../api';
import styles from './style.module.css';
import useAuthGuard from '../../context/useUser';
import SearchBar from '../../components/searchBar';
import { useToast } from '../../context/toast';

export default function Session(props) {
    const [students, setStudents] = useState(undefined);
    const [session, setSession] = useState(undefined);
    const [searchStudent, setSearchStudent] = useState(undefined)
    const token = useAuthGuard()
    const { toastList, setToastList } = useToast();

    const handleChange = (login) => {
        if (!students)
            return;
        students.forEach(element => {
            if (element.login === login) {
                let status = !element.status ? 'present' : null
                element.status = status;
            }
        });
    }

    const handleSearchChange = (event) => {
        setSearchStudent(students.filter((el) => el.login.includes(event.target.value)))
    }

    useEffect(() => {
        getSession(token, props.id).then((res) => {
            setStudents(res.students);
            setSession(res.session);
        })
    }, [token]);

    return (
        <>
            <section>
                <div class={`${styles.center} ${styles.buttonBox}`}>
                    <Button description="Allow session to be automatically signed." title="Validate" action={() => {
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
                    <Button description="Send all mails for the session." title="Send mail" action={() => {
                        modifySession(token, props.id, students).then((res) => {
                            signSession(token, props.id).then((res) => {
                                console.log(res)
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
                    }}></Button>
                    <Button description="Destroy and recreate session, fetching all students an other time." title="Refresh Session" action={() => {
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
                       ></StudentEntry> : null) : (students ? <StudentEntry
                         students={students}
                         onChange={handleChange}
                        ></StudentEntry> : null) 
                }
                </table>
            </section>
        </>
    )
}