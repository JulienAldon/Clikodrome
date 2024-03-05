import { useState } from "preact/hooks";
import useAuthGuard from "../../context/useUser";
import usePromotionStudent from "../../hooks/usePromotionStudent";
import styles from './style.module.css';
import { useTranslation } from "react-i18next";
import { editStudent } from "../../api";

export default function Promotion(props) {
    const { token, intraRole } = useAuthGuard(undefined);
    const { promotion, students, fetchPromotionStudent } = usePromotionStudent(props.id)
    const [ editElem, setEditElem ] = useState(undefined);
	const { t, i18n } = useTranslation();

    const handleShowEdit = (event) => {
        setEditElem(event.target.value);
        console.log(event.target.value);
    }

    const handleHideEdit = (index) => (event) => {
        setEditElem(undefined);
        editStudent(token, {card: event.target.value, id: index}, index).then((data) => {
            fetchPromotionStudent();
            // TODO show response state
        })
    }

    return (
        <>
        {
            promotion ?
            <section className={styles.pageBody}>
                <h2>{promotion.name}</h2>
                <ul className={styles.list}>
                    <li className={styles.tableHead}>
                        <label>Id</label>
                        <label>Login</label>
                        <label>Card</label>
                    </li>
                </ul>
                <ul className={styles.list}>
                {
                    students ? students.map((elem, index) => {
                        return (
                            <li key={index} className={styles.tableRow}>
                                <label>{elem.id}</label>
                                <label>{elem.login}</label>
                                {
                                    editElem == index ?
                                    <input type="text" value={elem.card} onBlur={handleHideEdit(elem.id)}/> :
                                    <button onClick={handleShowEdit} value={index} >{elem.card}</button>
                                } 
                            </li>
                        );
                    }) :    <li
                                className={styles.emptyTable}
                            >{t('No elements to display')}
                            </li>
                }
                </ul>
            </section> : null
        }
        </>
    );
}