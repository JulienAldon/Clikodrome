import { useEffect, useState } from "preact/hooks"
import { getPromotion } from "../api";
import { useAuth } from "../context/auth";

export default function useCityPromotion() {
    const [ cities, setCities ] = useState([]);

    const { token, intraRole} = useAuth()

    async function fetchCitiesPromotion() {
        getPromotion(token).then((res) => {
            setCities(prevPromotion => {
                let result = [...new Set(res.result.map(el => el.city))];
                return result;
            });
         })
    }

    useEffect(() => {
        fetchCitiesPromotion()
    }, [token])
    
    return {
        cities,
        fetchCitiesPromotion,
    }
}