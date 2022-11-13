import styles from './style.module.css';

export default function DateInput(props) {
    return (
        <div class={styles.center}>
            {/* <label class={styles.label}for="date" >{props.title}</label> */}
            <input 
                id="date"
                class={styles.search}
                title={props.description}
                onChange={props.onChange}
                type="date"
            />
        </div>
    );
}