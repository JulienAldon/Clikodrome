import styles from './style.module.css';

export default function TextInput(props) {
    return (
        <div class={`${props.class} ${styles.center}`}>
            <input 
                id={props.id}
                className={`${props.class} ${styles.search}`}
                title={props.description}
                onChange={props.onChange}
                placeholder={props.placeholder}
                type="text"
            />
        </div>
    );
}