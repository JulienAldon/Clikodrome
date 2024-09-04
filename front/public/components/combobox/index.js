import { useRef } from 'preact/hooks';
import styles from './style.module.css';

export default function ComboBox(props) {
    const inputRef = useRef()

    function handleClear() {
        if (inputRef.current)
            inputRef.current.value = null
        props.handleClear();
    }

    return (
        <div className={`${props.class} ${styles.center}`}>
            <input 
                ref={inputRef}
                onChange={props.onChange}
                id={props.id}
                className={`${styles.search}`}
                type="text"
                list={props.datalist_id}
                placeholder={props.title}
                title={props.title}
                value={props.value}
            />
            <datalist id={props.datalist_id}>
                {props.children}
            </datalist>
            <button onClick={handleClear} className={styles.close}></button>
        </div>
    );
}