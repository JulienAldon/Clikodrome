import styles from './style.module.css';

export function TableHead(props) {
    return (
        <th class={`${props.addStyle} ${styles.tablehead}`} onClick={props.sortFunction}>{props.title}
        { 
            props.toggleSort !== undefined ? 
            props.toggleSort ?
                <label class={`${styles.tablehead}`}> </label> : 
                <label class={`${styles.tablehead}`}> </label> : 
                <label class={`${styles.tablehead}`}> </label>
        }
        </th>
    );
}