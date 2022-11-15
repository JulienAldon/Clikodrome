import Toggle from '../../components/toggle';
import styles from './style.module.css';

export default function StudentEntry(props) {    
    return (
        <>
            {
                props.students.map((elem) => {
                    return (
                        <tr class={styles.box}>
                            <td class={styles.line}>
                                <label class={styles.label}>{elem.login}</label>
                            </td>
                            <td class={styles.padding}>
                                <Toggle description="Toggle if student has been seen for this session." login={elem.login} onChange={props.onChange} checked={elem.status === "present" || elem.status === "retard" ? true : false}></Toggle>
                            </td>
                            <td>
                                <Toggle description="Toggle if student has been late for this session, the time is automatically saved." login={elem.login} onChange={props.lateOnChange} checked={elem.late === "NULL" ? false : true}></Toggle>
                            </td>
                        </tr>
                    );
                })
            }
        </>
    );
}