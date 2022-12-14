import { useState } from "preact/hooks";
import { addRemote, removeRemote } from "../../api";
import Button from "../../components/button";
import ComboBox from "../../components/combobox";
import DateInput from "../../components/dateInput";
import { useToast } from "../../context/toast";
import useAuthGuard from "../../context/useUser";
import useRemotes from "../../hooks/useRemote";
import useStudents from "../../hooks/useStudents";
import styles from './style.module.css';

export default function Remote() {
    const token = useAuthGuard()
    
    const {toasList, setToastList} = useToast()

    const {students, fetchStudents} = useStudents()
    const {remoteStudents, fetchRemotes} = useRemotes()

    const [begin, setBegin] = useState(undefined)
    const [end, setEnd] = useState(undefined)
    const [student, setStudent] = useState(undefined)

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
                    title: "Info",
                    description: `Remote period added for ${student}.`,
                    backgroundColor: "rgba(15, 150, 150)",
                }]});
            })
        } else {
            setToastList((toastList) => {return [...toastList, {
                id: student,
                title: "Error",
                description: `Please fill out all input.`,
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
        <section>
            <div class={`${styles.remoteBox}`}>
                <h2 class={styles.center}>Remote Students</h2>
                <ComboBox 
                    title="Select student" 
                    onChange={handleStudentChange}>
                    {
                    students ?
                    students.map((el) => {
                        return (<option value={el}></option>);
                    }) : null
                    }
                </ComboBox>
                <DateInput
                    description="Date of the start of remote."
                    title="Begin"
                    onChange={handleBeginChange}
                />
                <DateInput
                    description="Date of the end of remote."
                    title="End"
                    onChange={handleEndChange}
                />
                <Button 
                    deactivated={false}
                    action={handleAddRemote} 
                    title="Add"
                    description="Add a new remote student."
                />
            </div>
            <table class={styles.centerCol}>
                <tr class={styles.box}>
                    <th title="Logins" class={styles.label}>Login</th>
                    <th title="Start date" class={styles.padding}>Start</th>
                    <th title="End date">End</th>
{/* TODO: Add a button to remove all remote entries */}
                    <th title="Remove"></th>
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
                                                title: "Info",
                                                description: `Remote period removed for ${el.login}.`,
                                                backgroundColor: "rgba(15, 150, 150)",
                                            }]});
                                        })
                                    }}
                                        class={styles.remove}
                                    >???</button>
                                </td>
                            </tr>
                        );
                        }) : null
                    }
            </table>
        </section>
    );
}