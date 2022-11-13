import { useState } from 'preact/hooks';
import Toggle from '../../components/toggle';
import styles from './style.module.css';

function addZero(i) {
    if (i < 10) {
        i = "0" + i
    }
    return i;
}

export default function StudentEntry(props) {
    const [students, setStudents] = useState([]);
    
    const lateOnChange = function(login) {
        const date = new Date();
        props.students.forEach(element => {
            if (element.login === login) {
                let status = !element.status ? 'retard' : null;
                let hour = !element.hour ? `${addZero(date.getHours())}:${addZero(date.getMinutes())}:00` : null;
                element.status = status;
                element.hour = hour;
            }
        });
        // console.log(props.students.find((l) => l.login === login))
    }

    return (
        <>
            {props.students.map((elem) => {
                return (
                    <tr class={styles.box}>
                        <td class={styles.line}>
                            <label class={styles.label}>{elem.login}</label>
                        </td>
                        <td class={styles.padding}>
                            <Toggle description="Toggle if student has been seen for this session." login={elem.login} onChange={props.onChange} checked={elem.status === "present" ? true : false}></Toggle>
                        </td>
                        <td>
                            <Toggle description="Toggle if student has been late for this session, the time is automatically saved." login={elem.login} onChange={lateOnChange} checked={elem.status === "retard" ? true : false}></Toggle>
                        </td>
                    </tr>
                );
            })}
        </>
    );
}