import styles from './style.module.css';

export default function Button(props) {
    return (
        <button 
            id={props.id}
            title={props.description} 
            className={`${props.class} ${styles.button} ${ props.deactivated || props.loading ? styles.deactivated : styles.activated }`} 
            onClick={props.action}
            disabled={props.deactivated || props.loading}
            onBlur={props.onBlur}
            onMouseDown={props.onMouseDown}
            value={props.id}
        >
            <label value={props.id} for={props.id}>{props.title}</label>
            {props.children}
            <div className={`${ props.loading ? styles.ldsEllipsis : ""}`}><div></div><div></div><div></div><div></div></div>
        </button>
    );
}