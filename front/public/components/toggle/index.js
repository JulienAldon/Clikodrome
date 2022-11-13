import styles from './style.module.css';

export default function Toggle(props) {
    return (
        <label title={props.description} class={styles.switchb}>
            <input onChange={() => {props.onChange(props.login)}} type="checkbox" checked={props.checked ? true : false}/>
            <span class={styles.slider}></span>
        </label>
    );
}