import styles from './style.module.css';

export default function Toggle(props) {
    return (
        <label title={props.description} class={styles.switchb}>
            <input id={props.login} onChange={(elem) => {props.onChange(elem.target.id)}} type="checkbox" checked={props.checked ? true : false}/>
            <span class={styles.slider}></span>
        </label>
    );
}