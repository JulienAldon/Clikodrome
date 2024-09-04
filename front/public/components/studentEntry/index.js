import Toggle from '../../components/toggle';
import styles from './style.module.css';

export default function StudentEntry(props) {    
    return (
        <>
            {
                props.students.map((elem) => {
                    return (
                        <tr id={elem.id} className={styles.box}>
                            <td className={styles.line}>
                                <label className={styles.label}>{elem.login}</label>
                            </td>
                            <td className={styles.padding}>
                                <Toggle description="Toggle if student has been seen at the begining of this session." login={elem.login} onChange={props.onChange(elem.login, "begin")} checked={elem.begin === "present" ? true : false}></Toggle>
                            </td>
                            <td className={styles.padding}>
                                <Toggle description="Toggle if student has been seen at the end of this session." login={elem.login} onChange={props.onChange(elem.login, "end")} checked={elem.end === "present" ? true : false}></Toggle>
                            </td>
                        </tr>
                    );
                })
            }
        </>
    );
}