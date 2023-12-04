import { useEffect, useState } from "preact/hooks"
import { getWeekplans } from "../api";
import { useAuth } from "../context/auth";

export default function useWeekplan() {
    const [ weekplans, setWeekplan ] = useState(undefined);
    const { token, intraRole} = useAuth()

    async function fetchWeekplan() {
        getWeekplans(token).then((res) => {
            setWeekplan(prevWeekplan => {
                let result = [];
                let ids = [...new Set(res.result.map(el => el.promotion_id))];
                ids.forEach((id) => {
                    result.push(res.result.filter((e) => {
                        return e.promotion_id === id;
                    }));
                });
                return result;
            });
         })
    }

    useEffect(() => {
        fetchWeekplan()
    }, [token])

    useEffect(() => {
      }, [weekplans]);
      

    return {
        weekplans,
        fetchWeekplan,
    }
}