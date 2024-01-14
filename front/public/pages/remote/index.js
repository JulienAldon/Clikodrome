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
import Volet from "../../components/volet";
import TableDisplay from "../../components/tableDisplay";

export default function Remote() {
    const { token, intraRole } = useAuthGuard("pedago");
    
    const {toasList, setToastList} = useToast()

    const {students, fetchStudents} = useStudents()
    const {remoteStudents, fetchRemotes} = useRemotes()
	const [ loadingRemoteList, setLoadingRemoteList ] = useState([]);

    const [ begin, setBegin ] = useState(undefined)
    const [ end, setEnd ] = useState(undefined)
    const [ student, setStudent ] = useState(undefined)

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
	
    const setElementInLoadingList = (index, value, setter, custom_list) => {
        const loadingTmp = [
            ...custom_list.slice(0, index),
            value, 
            ...custom_list.slice(index + 1)
        ];
        setter(loadingTmp);
    }

	const handleDeleteRemote = (index, event) => {
        if (!event.target.value) {
            return;
        }
        setElementInLoadingList(index, true, setLoadingRemoteList, loadingRemoteList);
        removeRemote(token, event.target.id).then((res) => {
            fetchRemotes();
            setToastList((toastList) => {return [...toastList, {
                id: 'a' + event.target.id,
                title: t("Information"),
                description: `${t('Remote period removed for')} ${event.target.id}.`,
                backgroundColor: "rgba(15, 150, 150)",
            }]});
            setElementInLoadingList(index, false, setLoadingRemoteList, loadingRemoteList);
        })
    }

    return (
        <section class={styles.pageBody}>
            <h1>{t('Manage Remote')}</h1>
            <Volet
                className={styles.center }
                title={t('Add remote')}
            >
                <div class={`${styles.remotePanel}`}>
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
            </Volet>
            <h2 class={styles.center}>{t('Remote Students')}</h2>
            {
                remoteStudents ? <TableDisplay
                    tableList={remoteStudents}
                    tableHead={[
                        {name: "Login", id: "login", stateIcon: ""},
                        {name: "Begin", id: "begin", stateIcon: ""},
                        {name: "End", id: "end", stateIcon: ""},
                        // {name: "City", id: "city", stateIcon: ""},
                    ]}
                    link={undefined}
                    loadingList={loadingRemoteList}
                    handleDeleteElement={handleDeleteRemote}
                /> : null
            }
        </section>
    );
}