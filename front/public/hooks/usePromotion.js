import { useEffect, useState } from "preact/hooks"
import { getPromotion } from "../api";
import { useAuth } from "../context/auth";

export default function usePromotion() {
    const [ promotions, setPromotion ] = useState(undefined);
    const { token, intraRole} = useAuth()

    async function fetchPromotion() {
        getPromotion(token).then((res) => {
            setPromotion(prevPromotion => {
                return res.result;
            });
         })
    }

    useEffect(() => {
        fetchPromotion()
    }, [token])

    useEffect(() => {
      }, [promotions]);
      

    return {
        promotions,
        fetchPromotion,
    }
}