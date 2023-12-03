import { useState } from "preact/hooks";
import useAuthGuard from "../../context/useUser";
import { useToast } from "../../context/toast";
import ComboBox from "../../components/combobox";
import { useTranslation } from "react-i18next";
import DateInput from "../../components/dateInput";
import Button from "../../components/button";
import { createPromotion, createWeekplan, removePromotion, removeWeekplan } from "../../api";
import usePromotion from "../../hooks/usePromotion";
import useWeekplan from "../../hooks/useWeekplan";
import styles from './style.module.css';

export default function Manager() {
    const token = useAuthGuard();
    const { toastList, setToastList } = useToast();
	const { t, i18n } = useTranslation();
    const [ promotion, setPromotion ] = useState("");
    const [ year, setYear ] = useState("");
    const allowed_promotions = ['wac1', 'wac2', 'premsc', 'msc1', 'msc2']
    const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    const { promotions, fetchPromotion } = usePromotion();
    const { weekplans, fetchWeekplan } = useWeekplan();
    const [ weekplanPromotion, setWeekplanPromotion ] = useState("");


    const handlePromotionChange = (event) => {
        setPromotion(event.target.value);
    }

    const handleYearChange = (event) => {
        let el = parseInt(event.target.value).toString()
        setYear(el);
    }

    const handleCreatePromotion = (event) => {
        if (year == "" || promotion == "") {
            setToastList((toastList) => {return [...toastList, {
                id: 1,
                title: t("Error"),
                description: t('Please fill out all input.'),
                backgroundColor: "rgba(150, 15, 15)",
            }]});
            return;
        }
        createPromotion(token, promotion, year).then((e) => {
            setToastList((toastList) => {return [...toastList, {
                id: 1,
                title: t("Information"),
                description: `${t('New promotion added')}.`,
                backgroundColor: "rgba(15, 150, 150)",
            }]});
            fetchPromotion();
        });
    }

    const handleDeletePromotion = (event) => {
        removePromotion(token, event.target.id).then((e) => {
            setToastList((toastList) => {return [...toastList, {
                id: 1,
                title: t("Information"),
                description: `${t('Promotion deleted')}.`,
                backgroundColor: "rgba(15, 150, 150)",
            }]});
            fetchPromotion();
        })
    }

    const handleDeleteWeekplan = (event) => {
        removeWeekplan(token, event).then((e) => {
            setToastList((toastList) => {return [...toastList, {
                id: 1,
                title: t("Information"),
                description: `${t('Weekplan deleted')}.`,
                backgroundColor: "rgba(15, 150, 150)",
            }]});
            fetchWeekplan();
        })
    }

    const handleAddWeekplan = (day) => {
        let promotion_id = promotions.filter(el => el.name === weekplanPromotion);
        if (promotion_id.length < 1) {
            setToastList((toastList) => {return [...toastList, {
                id: 1,
                title: t("Error"),
                description: `${t('Select a promotion first')}.`,
                backgroundColor: "rgba(150, 15, 15)",
            }]});
            return;
        }
        createWeekplan(token, day, promotion_id[0].id).then((res) => {
            setToastList((toastList) => {return [...toastList, {
                id: 1,
                title: t("Information"),
                description: `${t('Weekplan created')}.`,
                backgroundColor: "rgba(15, 150, 150)",
            }]});
            fetchWeekplan();
        })
    }

    const handleWeekplanPromotionText = (event) => {
        console.log(event.target.value);
        setWeekplanPromotion(event.target.value)
    }

    return (
        <section class="page-body">
            <h2>{t('Manage promotions')}</h2>
            <div className={styles.managerPanel}>
                <ComboBox 
                    class={styles.managerInputCombo}
                    title={t("Select promotion name")} 
                    onChange={handlePromotionChange}
                    datalist_id={"promotion_list"}>
                    {
                        allowed_promotions.map((el) => {
                            return <option value={el}></option>
                        })
                    }
                    
                </ComboBox>
                <DateInput
                    class={styles.managerInputDate}
                    description={t("Year of the promotion.")}
                    title={t("Year")}
                    onChange={handleYearChange}
                />
                <Button
                    deactivated={false}
                    action={handleCreatePromotion} 
                    title={t("Add")}
                    description={t("Add a new promotion.")}
                />
            </div>
            <h2>{t('Promotions')}</h2>
            {
                    promotions ? 
                    <ul>
                        {promotions.map((el) => {
                            return <li id={el.id}>
                                    <label>{el.name}_{el.year}</label>
                                    <Button
                                        class={`${styles.manageButton}`}
                                        id={el.id}
                                        deactivated={false}
                                        action={handleDeletePromotion} 
                                        title={"X"}
                                        description={t("Remove promotion.")}
                                    />
                                </li>
                        }) }
                    </ul> : null

                }
            <div id="weekplan">
                <table>
                    <caption>
                       {
                        promotions ?
                        <ComboBox 
                            title={t("Select promotion name")} 
                            onChange={handleWeekplanPromotionText}
                            datalist_id={"weekplan_list"}>
                            {
                                promotions.map((el) => {
                                    console.log(el)
                                    return <option id={el.id} value={el.name}></option>
                                })
                            }
                        </ComboBox>: null    
                    }
                    </caption>
                    <thead>
                        <tr>
                            <th>
                                <label>
                                    {t('Monday')}
                                </label>
                                <Button
                                    class={`${styles.manageButton}`}
                                    deactivated={false}
                                    action={() => {
                                        handleAddWeekplan("Monday")
                                    }} 
                                    title={"+"}
                                    description={t("Add")}
                                />
                            </th>
                            <th>
                                <label>
                                    {t('Tuesday')}
                                </label>
                                <Button
                                    class={`${styles.manageButton}`}
                                    deactivated={false}
                                    action={() => {
                                        handleAddWeekplan("Tuesday")
                                    }} 
                                    title={"+"}
                                    description={t("Add")}
                                />
                            </th>
                            <th>
                                <label>
                                    {t('Wednesday')}
                                </label>
                                <Button
                                    class={`${styles.manageButton}`}
                                    deactivated={false}
                                    action={() => {
                                        handleAddWeekplan("Wednesday")
                                    }} 
                                    title={"+"}
                                    description={t("Add")}
                                />
                            </th>
                            <th>
                                <label>
                                    {t('Thursday')}
                                </label>
                                <Button
                                    class={`${styles.manageButton}`}
                                    deactivated={false}
                                    action={() => {
                                        handleAddWeekplan("Thursday")
                                    }} 
                                    title={"+"}
                                    description={t("Add")}
                                />
                            </th>
                            <th>
                                <label>
                                    {t('Friday')}
                                </label>
                                <Button
                                    class={`${styles.manageButton}`}
                                    deactivated={false}
                                    action={() => {
                                        handleAddWeekplan("Friday")
                                    }} 
                                    title={"+"}
                                    description={t("Add")}
                                />
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        {
                            weekplans && promotions ? 
                            weekplans.map((plans) => {
                                return (
                                    <tr>
                                        {
                                            days.map((day) => {
                                                let current_plan = plans.filter(el => el.day === day);
                                                if (current_plan.length < 1) {
                                                    return <td></td>;
                                                }
                                                let elem = promotions.filter(e => e.id === current_plan[0].promotion_id)
                                                if (elem.length < 1) {
                                                    return <td></td>;
                                                }
                                                console.log(elem)
                                                return (
                                                    <td>
                                                        <label>{elem[0].name}</label>
                                                        <Button
                                                            class={`${styles.manageButton}`}
                                                            deactivated={false}
                                                            action={handleDeleteWeekplan} 
                                                            title={"X"}
                                                            description={t("Remove")}
                                                        />
                                                    </td>);
                                            })
                                        }
                                    </tr>
                                );
                            }) : null
                        }
                    </tbody>
                </table>
            </div>
        </section>
    );
}