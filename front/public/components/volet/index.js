import { useState } from "preact/hooks";
import styles from "./style.module.css";

export default function Volet(props) {
    const [show, setShow] = useState(false);

    return (
        <div className={props.className}>
            <button className={`${styles.button}`} onClick={() => {
                setShow(!show);
            }}><span className={styles.icon}>{show ? "" : ""}</span><h2 className={styles.title}>{props.title}</h2></button>
            <div className={`${styles.content} ${show ? "" : styles.hide}`}>
                {props.children}
            </div>
        </div>
    );
}