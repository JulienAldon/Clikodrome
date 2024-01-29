import { useState } from "preact/hooks";
import useAuthGuard from "../../context/useUser";
import usePromotionStudent from "../../hooks/usePromotionStudent";
import styles from './style.module.css';
import { useTranslation } from "react-i18next";

export default function Promotion(props) {
    const { token, intraRole } = useAuthGuard(undefined);
    const { promotion, students, fetchPromotionStudent } = usePromotionStudent(props.id)
    const [ editElem, setEditElem ] = useState();
	const { t, i18n } = useTranslation();

    const handleShowEdit = (event) => {
        setEditElem(event.target.value);
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
                            <li className={styles.tableRow}>
                                <label>{elem.id}</label>
                                <label>{elem.login}</label>
                                {editElem === index ? <label onClick={handleShowEdit}>{elem.card}</label> : <input type="text" value={elem.card}></input>}
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