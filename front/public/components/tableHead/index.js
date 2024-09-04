import styles from './style.module.css';

export function TableHead(props) {
    return (
        <th className={`${props.addStyle} ${styles.tablehead}`} onClick={props.sortFunction}>{props.title}
        { 
            props.toggleSort !== undefined ? 
            props.toggleSort ?
                <label className={`${styles.tablehead}`}> </label> : 
                <label className={`${styles.tablehead}`}> </label> : 
                <label className={`${styles.tablehead}`}> </label>
        }
        </th>
    );
}