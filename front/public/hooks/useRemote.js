import { useEffect, useState } from "preact/hooks";
import { getRemotes } from "../api";
import { useAuth } from "../context/auth";

export default function useRemotes() {
    const [remoteStudents, setRemoteStudents] = useState(undefined);
    const token = useAuth();
    
    async function fetchRemotes() {
        getRemotes(token).then((res) => {
            if (res.result) {
                setRemoteStudents(res.result)
            }
        })
    }

    useEffect(() => {
        fetchRemotes()
    }, [token])

    return {remoteStudents, fetchRemotes}
}