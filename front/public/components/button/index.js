import styles from './style.module.css';

export default function Button(props) {
    return (
        <button 
            title={props.description} 
            class={`${styles.button} ${ props.deactivated ? styles.deactivated : styles.activated }`} 
            onClick={props.action}
            disabled={props.deactivated}
        >
            {props.title}
        </button>
    );
}