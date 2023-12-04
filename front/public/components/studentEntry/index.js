import Toggle from '../../components/toggle';
import styles from './style.module.css';

export default function StudentEntry(props) {    
    return (
        <>
            {
                props.students.map((elem) => {
                    return (
                        <tr id={elem.id} class={styles.box}>
                            <td class={styles.line}>
                                <label class={styles.label}>{elem.login}</label>
                            </td>
                            <td class={styles.padding}>
                                <Toggle description="Toggle if student has been seen for this session." login={elem.login} onChange={props.onChange} checked={elem.status === "present" ? true : false}></Toggle>
                            </td>
                        </tr>
                    );
                })
            }
        </>
    );
}