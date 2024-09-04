import { useRef } from 'preact/hooks';
import styles from './style.module.css';

export default function SearchBar(props) {
    const inputRef = useRef();

    function handleClear() {
        if (inputRef.current)
            inputRef.current.value = null;
        props.onClear();
    }

    return (
        <>
            <div className={styles.searchContainer}>
                <input 
                    ref={inputRef}
                    id="search" 
                    onInput={props.onChange} 
                    className={styles.search} 
                    type="search" 
                    title={props.description} 
                    placeholder={props.placeholder}>
                </input>
                <button onClick={handleClear} className={styles.close}></button>
            </div>
        </>
    );
}