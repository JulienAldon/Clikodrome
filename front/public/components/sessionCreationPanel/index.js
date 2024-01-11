import { useTranslation } from "react-i18next";
import Button from "../button";
import ComboBox from "../combobox";
import DateInput from "../dateInput";
import styles from "./style.module.css";

const sessionCreationPanel = ({cities, cityProps, periodProps, dateProps, loadingSession, handleCreateSession, show}) => {
	const halfDay = ['Morning', 'Evening']
	const { t, i18n } = useTranslation();

    return (
    <div className={`${styles.controlBox} ${!show ? styles.show : null}`}>
        <div className={styles.formBox}>
            {
            cities ?
            <ComboBox
                class={styles.sessionInputCombo}
                title={t("Enter city")}
                {...cityProps}
                handleClear={cityProps.resetFormValue}
                datalist_id={"citySelect_list"}>
                {
                    cities.map((el) => {
                        return <option id={el} value={el}>{el}</option>
                    })
                }
            </ComboBox> : null
            }
            <DateInput
                class={styles.sessionDateSelect}
                description={t("Date of the session")}
                title={t("Date")}
                {...dateProps}
            >
            </DateInput>
            <ComboBox
                class={styles.sessionInputCombo}
                title={t('Select half day')}
                {...periodProps}
                handleClear={periodProps.resetFormValue}
                datalist_id={"day_time"}
            >
            {
                halfDay.map((el) => {
                    return (<option value={el}></option>);
                })
            }
            </ComboBox>
        </div>
        <Button
            class={styles.createButton}
            deactivated={(periodProps.value === "" || periodProps.value === null || dateProps.value === "" || dateProps.value === null || cityProps.value === "" || cityProps.value === null) ? true : false}
            description={t('Create session')}
            title={"+"}
            loading={loadingSession}
            action={handleCreateSession}>
        </Button>
    </div>
    )
}

export default sessionCreationPanel;