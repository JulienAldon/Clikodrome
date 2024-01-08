import { useEffect, useState } from "preact/hooks"
import { getWeekplans } from "../api";
import { useAuth } from "../context/auth";

export default function useCityWeekplan() {
    const [ cities, setCities ] = useState([]);

    const { token, intraRole} = useAuth()

    async function fetchCitiesWeekplan() {
        getWeekplans(token).then((res) => {
            setCities(prevWeekplan => {
                let result = [];
                let ids = [...new Set(res.result.map(el => el.city))];
                ids.forEach((id) => {
                    result.push(res.result.filter((e) => {
                        return e.city === id;
                    })[0].city);
                });
                return result;
            });
         })
    }

    useEffect(() => {
        fetchCitiesWeekplan()
    }, [token])
    
    return {
        cities,
        fetchCitiesWeekplan,
    }
}