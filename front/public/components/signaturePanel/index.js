import styles from './style.module.css';

export default function({signLinks, show, refetchSignList, isRefetching}) {
    return (
        <div className={`${styles.signBox} ${!show ? styles.show : null}`}>
            {
                signLinks ? 
                <ul>

                    { signLinks.map((elem) => {
                        return (
                            <li key={elem.sign_id} className={styles.signElement}>                                
                                <button 
                                    className={styles.buttonSignList}
                                    onClick={refetchSignList}
                                >
                                { 
                                    isRefetching ? 
                                    <label className={styles.signLoader}></label> :
                                    elem.state ? 
                                    <label className={styles.signOk}></label> : 
                                    <label className={styles.signKo}></label>
                                }
                                </button>
                                <a 
                                    target="_blank"
                                    className={styles.linkElement}
                                    href={elem.link}
                                >
                                    <label>{elem.session_name}</label>
                                </a>
                            </li>
                        );
                    })
                    }
                </ul> : null
            }
        </div>
    );
}