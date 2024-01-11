import { useState } from "preact/hooks";
import { addRemote, removeRemote } from "../../api";
import { useToast } from "../../context/toast";
import { useTranslation } from 'react-i18next';
import Button from "../../components/button";
import ComboBox from "../../components/combobox";
import DateInput from "../../components/dateInput";
import useAuthGuard from "../../context/useUser";
import useRemotes from "../../hooks/useRemote";
import useStudents from "../../hooks/useStudents";
import styles from './style.module.css';

export default function Remote() {
    const { token, intraRole } = useAuthGuard("pedago");
    
    const {toasList, setToastList} = useToast()

    const {students, fetchStudents} = useStudents()
    const {remoteStudents, fetchRemotes} = useRemotes()

    const [ begin, setBegin ] = useState(undefined)
    const [ end, setEnd ] = useState(undefined)
    const [ student, setStudent ] = useState(undefined)
    const [ showControl, setShowControl ] = useState(false)

	const { t, i18n } = useTranslation();

    function handleStudentChange(event) {
        if (event.target.value)
            setStudent(event.target.value)
    }
    
    function handleAddRemote(event) {
        if (begin && end && student) {
            addRemote(token, {login: student, begin: begin, end:end}).then((res) => {
                fetchRemotes();
                setToastList((toastList) => {return [...toastList, {
                    id: student,
                    title: t("Information"),
                    description: `${t('Remote period added for')} ${student}.`,
                    backgroundColor: "rgba(15, 150, 150)",
                }]});
            })
        } else {
            setToastList((toastList) => {return [...toastList, {
                id: student,
                title: t("Error"),
                description: t('Please fill out all input.'),
                backgroundColor: "rgba(150, 15, 15)",
            }]});
        }
    }

    function handleBeginChange(event) {
        if (event.target.value)
            setBegin(event.target.value)
    }

    function handleEndChange(event) {
        if (event.target.value)
            setEnd(event.target.value)
    }

    return (
        <section class="page-body">
            <h2 class={styles.center}
                onClick={() => setShowControl(!showControl)}
            >{t('Remote Students')}</h2>
            <div class={`${styles.remoteBox} ${!showControl ? styles.show : null}`}
            >
                <ComboBox 
                    handleClear={() => {}}
                    title={t("Select student")} 
                    onChange={handleStudentChange}
                    datalist_id={"remote_list"}>
                    {
                    students ?
                    students.map((el) => {
                        return (<option value={el}></option>);
                    }) : null
                    }
                </ComboBox>
                <DateInput
                    description={t("Date of the start of remote.")}
                    title={t("Begin")}
                    onChange={handleBeginChange}
                />
                <DateInput
                    description={t("Date of the end of remote.")}
                    title={t("End")}
                    onChange={handleEndChange}
                />
                <Button 
                    deactivated={false}
                    action={handleAddRemote} 
                    title={t("Add")}
                    description={t("Add a new remote student.")}
                />
            </div>
            <h2 class={styles.center}>{t('Remote Students')}</h2>
            <table class={styles.centerCol}>
                <tr class={styles.box}>
                    <th title={t("Login")} class={styles.label}>{t('Login')}</th>
                    <th title={t("Start date")} class={styles.padding}>{t('Begin')}</th>
                    <th title={t("End date")}>{t('End')}</th>
                    <th title={t("Remove")}></th>
                </tr>
                    {
                        remoteStudents ? 
                        remoteStudents.map((el) => {
                        return (
                            <tr class={styles.box}>
                                <td title={el.login} class={styles.label}>{el.login}</td>
                                <td title={el.begin} class={styles.padding}>{el.begin}</td>
                                <td title={el.end}>{el.end}</td>
                                <td>
                                    <button onClick={() => {
                                        removeRemote(token, el.id).then((res) => {
                                            fetchRemotes();
                                            setToastList((toastList) => {return [...toastList, {
                                                id: 'a' + el.id,
                                                title: t("Information"),
                                                description: `${t('Remote period removed for')} ${el.login}.`,
                                                backgroundColor: "rgba(15, 150, 150)",
                                            }]});
                                        })
                                    }}
                                        class={styles.remove}
                                    ></button>
                                </td>
                            </tr>
                        );
                        }) : null
                    }
            </table>
        </section>
    );
}