import { useEffect, useState } from "preact/hooks";
import { checkTodaySession } from "../api";
import { useAuth } from "../context/auth";

export default function useSessionStatus() {
    const [sessionStatus, setSessionStatus] = useState(undefined);
    const { token, intraRole} = useAuth()
    
    async function fetchSessionStatus() {
        checkTodaySession(token).then((res) => {
            if (res.result) {
                setSessionStatus(res.result)
            }
        })
    }

    useEffect(() => {
        fetchSessionStatus()
    }, [token])

    return {sessionStatus, fetchSessionStatus}
}