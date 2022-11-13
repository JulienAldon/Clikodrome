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
            <div class={styles.searchContainer}>
                <input 
                    ref={inputRef}
                    id="search" 
                    onInput={props.onChange} 
                    class={styles.search} 
                    type="search" 
                    title={props.description} 
                    placeholder={props.placeholder}>
                </input>
                <button onClick={handleClear} class={styles.close}></button>
            </div>
        </>
    );
}