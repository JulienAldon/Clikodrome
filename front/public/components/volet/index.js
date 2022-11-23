import { useState } from "preact/hooks";
import styles from "./style.module.css";

export default function Volet(props) {
    const [show, setShow] = useState(false);

    return (
        <>
            <button class={styles.button} onClick={() => {
                setShow(!show);
            }}><h2 class={styles.title}>{props.title}</h2><span class={styles.icon}>{show ? "" : ""}</span></button>
            <div class={`${styles.content} ${show ? "" : styles.hide}`}>
                {props.children}
            </div>
        </>
    );
}