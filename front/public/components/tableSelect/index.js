import { useEffect, useState } from 'preact/hooks';
import Button from '../button';
import styles from './style.module.css';
import { useTranslation } from 'react-i18next';

export default function TableSelect({tableList, tableHead, defaultSort="id", link, loadingList, handleDeleteElement, handleSelectElement}) {
    const [ sortedList, setSortedList ] = useState([...tableList]);
    const [ tableHeadData, setTableHeadData ] = useState([...tableHead]);
	const { t, i18n } = useTranslation();

    function setHeadStateIcon(table, icon, elem) {
        let newTable = table.map((el => {
            return {...el, stateIcon: ""}
        }));
        newTable.find((el) => el.id == elem).stateIcon = icon;
        return newTable;
    }

    function sortTable(toSort, order) {
        return function (a, b) {
            let x;
            let y;

            if (toSort === "id") {
                x = parseInt(a[toSort]);
                y = parseInt(b[toSort]);
            } else {
                x = a[toSort].toLowerCase();
                y = b[toSort].toLowerCase();
            }
            if (x < y) {return order;}
            if (x > y) {return -order;}
            return 0;
        };
    }

    function sortElements(sortElement) {
        let arr = [...sortedList];
        let tmp = [...arr];
        arr.sort(sortTable(sortElement, 1));
        setTableHeadData(setHeadStateIcon(tableHeadData, "", sortElement));
        if (JSON.stringify(arr) === JSON.stringify(tmp)) {
            arr.sort(sortTable(sortElement, -1));
            setTableHeadData(setHeadStateIcon(tableHeadData, "", sortElement));
        }
        setSortedList(arr);
    }

    useEffect(() => {
        setSortedList(tableList);
        setTableHeadData(tableHead);
    }, [tableList, tableHead]);

    return (
        <>
            <ul className={styles.list}>
                <li
                    className={styles.tableHead}
                >
                     <div className={styles.headCell}>
                        <label>Select</label>
                    </div>
                    {tableHeadData.map((t) => {
                        return (
                            <button
                                className={styles.headCell}
                                onClick={() => {
                                    sortElements(t.id)
                                }}
                            >
                                <label className={styles.item} key={t.id}>{t.name} {t.stateIcon}</label>
                            </button>
                        );
                    })}
                    <div className={styles.headCell}>
                        <label>Action</label>
                    </div>
                </li>
            </ul>
            <ul className={styles.list}>
                {sortedList && sortedList.length > 0 ? sortedList.map((elem, index) => {
                    return (
                        <li 
                            className={`${styles.tableRow}`}
                            key={elem.id}
                        >
                            <input className={styles.licell} value={elem.id} onClick={handleSelectElement} type="checkbox"/>
                            <a
                                href={link ? link+elem.id : null}
                                className={styles.a}
                            >
                                {tableHeadData.map((t) => {
                                    return (
                                        <label className={`${styles.licell} ${styles.item}`} key={t.id}>{elem[t.id]}</label>
                                    );
                                })}
                            </a>
                            <div className={`${styles.licell} ${styles.deleteButtonCell}`}>
                                <Button
                                    className={styles.deleteButton}
                                    id={elem.id}
                                    value={elem.id}
                                    title={""}
                                    deactivated={false}
                                    loading={loadingList[index]}
                                    action={(event) => {
                                        handleDeleteElement(index, event)
                                    }}
                                ></Button>
                            </div>
                        </li>
                    );
                }) : <li
                        className={styles.emptyTable}
                    >
                        {t('No elements to display')}
                    </li>}
            </ul>
        </>
    );
}