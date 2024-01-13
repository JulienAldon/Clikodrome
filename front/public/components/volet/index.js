import { useState } from "preact/hooks";
import styles from "./style.module.css";

export default function Volet(props) {
    const [show, setShow] = useState(false);

    return (
        <div className={props.className}>
            <button className={`${styles.button}`} onClick={() => {
                setShow(!show);
            }}><span class={styles.icon}>{show ? "" : ""}</span><h2 class={styles.title}>{props.title}</h2></button>
            <div class={`${styles.content} ${show ? "" : styles.hide}`}>
                {props.children}
            </div>
        </div>
    );
}