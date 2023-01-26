import styles from './style.module.css';

export default function Button(props) {
    return (
        <button 
            title={props.description} 
            class={`${styles.button} ${ props.deactivated || props.loading ? styles.deactivated : styles.activated }`} 
            onClick={props.action}
            disabled={props.deactivated || props.loading}
        >
            {props.title}
            <div class={`${ props.loading ? styles.ldsEllipsis : ""}`}><div></div><div></div><div></div><div></div></div>
        </button>
    );
}