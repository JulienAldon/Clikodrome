import { useState, useEffect } from "preact/hooks";
import useAuthGuard from "../../context/useUser";
import { useToast } from "../../context/toast";
import ComboBox from "../../components/combobox";
import { useTranslation } from "react-i18next";
import TextInput from "../../components/textInput";
import Button from "../../components/button";
import { createPromotion, createWeekplan, removePromotion, removeWeekplan } from "../../api";
import usePromotion from "../../hooks/usePromotion";
import useWeekplan from "../../hooks/useWeekplan";
import styles from './style.module.css';
import useGroup from "../../hooks/useGroup";
import useCityFilter from "../../hooks/useCityFilter";
import useFormInput from "../../hooks/useFormInput";

export default function Manager() {
    const { token, intraRole } = useAuthGuard("pedago");
    const { toastList, setToastList } = useToast();
	const { t, i18n } = useTranslation();
    
    const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    
    const yearProps = useFormInput();
    const cityProps = useFormInput();
    const promotionProps = useFormInput();
    const { groups, fetchEdusignGroup } = useGroup();
    const { promotions, fetchPromotion } = usePromotion();
    
    const { weekplans, fetchWeekplan } = useWeekplan();
    const [ weekplansShow, setWeekPlansShow ] = useState([]);
    const [ weekplanPromotion, setWeekplanPromotion ] = useState([]);
    const [ loadingAddPromotion, setLoadingAddPromotion ] = useState(false);
    const [ loadingPromotionList, setLoadingPromotionList ] = useState([]);

    const {
        filteredList: promotionShow,
        cityFilter: cityFilter,
        setCityFilter: setCityFilter, 
        handleCityFilterChange: handleCityFilterChange,
        cities: cities
    } = useCityFilter({sourceList:promotions});

    const setElementInLoadingList = (index, value, setter, custom_list) => {
        const loadingTmp = [
            ...custom_list.slice(0, index),
            value, 
            ...custom_list.slice(index + 1)
        ];
        setter(loadingTmp);
    }

    const handleCreatePromotion = (event) => {
        if (yearProps.value === "" || promotionProps.value === "" || cityProps.value === "") {
            setToastList((toastList) => {return [...toastList, {
                id: 1,
                title: t("Error"),
                description: t('Please fill out all input.'),
                backgroundColor: "rgba(150, 15, 15)",
            }]});
            return;
        }
        let sign_obj = groups.filter((e) => {return e.name === promotionProps.value})[0]
        if (sign_obj === undefined) {
            setToastList((toastList) => {return [...toastList, {
                id: 1,
                title: t("Error"),
                description: t('Please use a correct edusign promotion.'),
                backgroundColor: "rgba(150, 15, 15)",
            }]});
            return
        }
        setLoadingAddPromotion(true);
        createPromotion(token, promotionProps.value, yearProps.value, sign_obj.id, cityProps.value).then((e) => {
            setToastList((toastList) => {return [...toastList, {
                id: 1,
                title: t("Information"),
                description: `${t('New promotion added')}.`,
                backgroundColor: "rgba(15, 150, 150)",
            }]});
            fetchPromotion();
            setLoadingAddPromotion(false);
        });
    }

    const handleDeletePromotion = (index) => (event) => {
        if (!event.target.value) {
            return;
        }
        setElementInLoadingList(index, true, setLoadingPromotionList, loadingPromotionList);
        removePromotion(token, event.target.value).then((e) => {
            setToastList((toastList) => {return [...toastList, {
                id: 1,
                title: t("Information"),
                description: `${t('Promotion deleted')}.`,
                backgroundColor: "rgba(15, 150, 150)",
            }]});
            fetchPromotion();
            setElementInLoadingList(index, false, setLoadingPromotionList, loadingPromotionList);
        })
    }

    const handleDeleteWeekplan = (event) => {
        if (!event.target.value) {
            return;
        }
        removeWeekplan(token, event.target.value).then((e) => {
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
        if (weekplanPromotion.length < 1) {
            setToastList((toastList) => {return [...toastList, {
                id: 1,
                title: t("Error"),
                description: `${t('Select a promotion first')}.`,
                backgroundColor: "rgba(150, 15, 15)",
            }]});
            return;
        }
        weekplanPromotion.map((e) => {
            if (e.selected) {
                createWeekplan(token, day, e.id).then((res) => {
                    setToastList((toastList) => {return [...toastList, {
                        id: 1,
                        title: t("Information"),
                        description: `${t('Weekplan created')}.`,
                        backgroundColor: "rgba(15, 150, 150)",
                    }]});
                    fetchWeekplan();
                })
            }
        });
    }

    const handleWeekplanSelectPromotion = (event) => {
        let current = weekplanPromotion.filter((e) => e.id === event.target.value)[0];
        if (current) {
            let newList = weekplanPromotion.map((e) => {
                if (e.id === event.target.value) {
                    e.selected = !e.selected;
                };
                return e;
            });
            setWeekplanPromotion(newList);
        } else {
            setWeekplanPromotion(oldArr => [...oldArr, {'id': event.target.value, 'selected': true}]);
        }
    }

    useEffect(() => {
        if (cityFilter === "" || cityFilter === null) {
            setWeekPlansShow(weekplans);
            return
        }
        let newWp = weekplans.filter((e) => {
            return e[0].city === cityFilter
        });
        setWeekPlansShow([...newWp]);
    }, [ cityFilter, weekplans ]);

    return (
        <section className={styles.pageBody}>
            <h1>{t('Manage promotions')}</h1>
            {
                cities ?
                <ComboBox 
                    class={styles.managerInputCombo}
                    title={t("Filter by city")}
                    onChange={handleCityFilterChange}
                    handleClear={() => {
                        setCityFilter("");
                    }}
                    datalist_id={"city_list"}>
                    {
                        cities.map((el) => {
                            return <option id={el} value={el}>{el}</option>
                        })
                    }
                </ComboBox> : null
            }
            <div className={styles.managerPanel}>
                
                <div>
                    <h2>{t('Add Promotion')}</h2>
                    <ComboBox 
                        {...promotionProps}
                        class={styles.managerInputCombo}
                        title={t("Select promotion name")} 
                        datalist_id={"promotion_list"}
                        handleClear={() => {}}
                    >
                        {
                            groups.map((el) => {
                                return <option id={el.id} value={el.name}>{el.name}</option>
                            })
                        }
                        
                    </ComboBox>
                    <TextInput
                        {...yearProps}
                        id="year"
                        class={styles.managerInputDate}
                        description={t("Year of the promotion.")}
                        title={t("Year")}
                        placeholder={t("Enter year")}
                    />
                    <TextInput
                        {...cityProps}
                        id="city"
                        class={styles.managerInputDate}
                        title={t('Enter city linked to promotion')}
                        placeholder={t('Enter city')}
                    />
                </div>
                <div className={styles.managerAddButton}>
                    <Button
                        class={styles.manageButton}
                        deactivated={false}
                        loading={loadingAddPromotion}
                        action={handleCreatePromotion} 
                        title={"+"}
                        description={t("Add a new promotion.")}
                    />
                </div>
                <div className={styles.promotionBox}>
                    <h2>{t('Promotions')}</h2>
                    {
                        promotionShow ? 
                        <ul className={styles.ul}>
                            {promotionShow.map((el, index) => {
                                return <li className={styles.li} id={el.id}>
                                        <input value={el.id} onClick={handleWeekplanSelectPromotion} type="checkbox" id="select"/>
                                        <label for="select">{el.name}_{el.year}</label>
                                        <Button
                                            class={`${styles.manageButton}`}
                                            id={el.id}
                                            value={el.id}
                                            deactivated={false}
                                            loading={loadingPromotionList[index]}
                                            action={handleDeletePromotion(index)}
                                            title={"X"}
                                            description={t("Remove promotion.")}
                                        />
                                    </li>
                            }) }
                        </ul> : null
                    }
                </div>
            </div>

            <div id="weekplan">
                <h2>{t('Manage Weekplans')}</h2>
                <table className={styles.table}>
                    <caption>
                        <span>{t('Select promotions above and assign to week days.')}</span>
                    </caption>
                    <thead>
                        <tr className={styles.tr}>
                            {
                                days.map((elem) => {
                                    return (
                                        <th className={styles.th}>
                                            <label>
                                                {t(elem)}
                                            </label>
                                            <Button
                                                class={`${styles.manageButton}`}
                                                deactivated={false}
                                                action={() => {
                                                    handleAddWeekplan(elem)
                                                }} 
                                                title={"+"}
                                                description={t("Add")}
                                            />
                                        </th>
                                    );
                                })
                            }
                        </tr>
                    </thead>
                    <tbody>
                        {
                            weekplansShow && promotions ? 
                            weekplansShow.map((plans) => {
                                return (
                                    <tr className={styles.tr}>
                                        {
                                            days.map((day) => {
                                                let current_plan = plans.filter(el => el.day === day);
                                                if (current_plan.length < 1) {
                                                    return <td className={styles.td}></td>;
                                                }
                                                let elem = promotions.filter(e => e.id === current_plan[0].promotion_id)
                                                if (elem.length < 1) {
                                                    return <td className={styles.td}></td>;
                                                }
                                                return (
                                                    <td className={styles.td}>
                                                        <label for={current_plan[0].id}>{elem[0].name}</label>
                                                        <Button
                                                            id={current_plan[0].id}
                                                            class={`${styles.manageButton}`}
                                                            deactivated={false}
                                                            action={handleDeleteWeekplan} 
                                                            title={"X"}
                                                            description={t("Remove")}
                                                        />
                                                    </td>
                                                );
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