import { useState, useEffect } from "react";
import styles from './style.module.css';
import Button from "../button";

const SessionsTable = ({sessionList, sessionHead, defaultSort="id", loadingList, handleDeleteElement}) => {
    const [ sortedList, setSortedList ] = useState([...sessionList]);
    const [ tableHeadData, setTableHeadData ] = useState([...sessionHead]);

    function setHeadStateIcon(table, icon, elem) {
        let newTable = table.map((el => {
            return {...el, stateIcon: ">"}
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
        setTableHeadData(setHeadStateIcon(tableHeadData, "v", sortElement));
        if (JSON.stringify(arr) === JSON.stringify(tmp)) {
            arr.sort(sortTable(sortElement, -1));
            setTableHeadData(setHeadStateIcon(tableHeadData, "^", sortElement));
        }
        setSortedList(arr);
    }

    useEffect(() => {
        setSortedList(sessionList);
        setTableHeadData(sessionHead);
    }, [sessionList, sessionHead]);

    return (
        <>
            <ul className={styles.list}>
                <li
                    className={styles.tableHead}
                >
                    {tableHeadData.map((t) => {
                        return (
                            <button
                                className={styles.filterButton}
                                onClick={() => {
                                    sortElements(t.id)
                                }}
                            >
                                <label className={styles.item} key={t.id}>{t.name}</label>
                                {t.stateIcon}    
                            </button>
                        );
                    })}
                    <div className={styles.filterButton}>
                        <label>Action</label>
                    </div>
                </li>
            </ul>
            <ul className={styles.list}>
                {sortedList ? sortedList.map((elem, index) => {
                    return (
                        <li 
                            className={styles.tableRow}
                            key={elem.id}>
                            <a
                                href={"/session/"+elem.id}
                                className={styles.a}
                            >
                                {tableHeadData.map((t) => {
                                    return (
                                        <label className={styles.item} key={t.id}>{elem[t.id]}</label>
                                    );
                                })}
                                 
                            </a>
                            <div className={styles.deleteButtonCell}>
                                <Button
                                        class={styles.deleteButton}
                                        id={elem.id}
                                        value={elem.id}
                                        title={"X"}
                                        deactivated={false}
                                        loading={loadingList[index]}
                                        action={(event) => {
                                            handleDeleteElement(index, event)
                                            event.stopPropagation();
                                        }}
                                ></Button>
                            </div>
                        </li>
                    );
                }) : <></>}
            </ul>
        </>
    );
}

export default SessionsTable;