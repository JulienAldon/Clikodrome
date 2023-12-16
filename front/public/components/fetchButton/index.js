import { useTranslation } from "react-i18next";
import Button from "../button";
import { useState, useRef } from "preact/hooks";
import styles from './style.module.css';

export default function fetchButton(props) {
	const { t, i18n } = useTranslation();
    const [ isFetchInput, setIsFetchInput ] = useState(true);
    const [ fetchInput, setFetchInput ] = useState("");
    const fetchText = useRef();
    const fetchButton = useRef();

    return (
        <Button 
            deactivated={false} 
            description={t("Fetch session presence status from epitech intranet")} 
            title={t("Fetch from intra")} 
            loading={props.refreshLoading}
            action={(e) => {
                setIsFetchInput(!isFetchInput);
            }}
            onBlur={(e) => {
                const currentTarget = e.currentTarget;
                requestAnimationFrame(() => {
                    if (!currentTarget.contains(document.activeElement)) {
                        setIsFetchInput(true);
                    }
                });
            }}
        >
            <input ref={fetchText} type="text" onClick={(e) => {
                e.stopPropagation();
            }} onChange={(e) => {
                setFetchInput(e.target.value);
            }} placeholder={t("Enter activity url")} hidden={isFetchInput}></input>
            <input className={styles.queryButton} ref={fetchButton} type="button" value="Ok" onClick={(e) => {
                e.stopPropagation();
                props.command(props.id, fetchInput);
                setTimeout(() => {
                    setIsFetchInput(true);
                });
            }} hidden={isFetchInput}/>
        </Button>
    );
}