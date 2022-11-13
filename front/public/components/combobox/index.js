import { useRef } from 'preact/hooks';
import styles from './style.module.css';

export default function ComboBox(props) {
    const inputRef = useRef()

    function handleClear() {
        if (inputRef.current)
            inputRef.current.value = null
    }
    return (
        <div class={styles.center}>
            <input 
                ref={inputRef}
                onChange={props.onChange}
                id="input"
                class={styles.search}
                type="text"
                list="elements"
                placeholder={props.title}
                title={props.title}
            />
            <datalist id="elements">
                {props.children}
            </datalist>
            <button onClick={handleClear} class={styles.close}></button>
        </div>
    );
}