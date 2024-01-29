import { useEffect, useState } from "preact/hooks"
import { getPromotion } from "../api";
import { useAuth } from "../context/auth";

export default function usePromotionStudent(id) {
    const [ promotion, setPromotion ] = useState(undefined);
    const [ students, setStudent ] = useState(undefined);
    const { token, intraRole} = useAuth()

    async function fetchPromotionStudent() {
        getPromotion(id, token).then((res) => {
            setPromotion(prevPromotion => {
                return res.result.promotion;
            });
            setStudent(prevStudent => {
                return res.result.students;
            });
         })
    }

    useEffect(() => {
        fetchPromotionStudent()
    }, [token])

    return {
        promotion,
        students,
        fetchPromotionStudent,
    }
}