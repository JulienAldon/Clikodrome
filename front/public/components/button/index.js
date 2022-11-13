import styles from './style.module.css';

export default function Button(props) {
    return (
        <button title={props.description} class={styles.button} onClick={props.action}>
            {props.title}
        </button>
    );
}