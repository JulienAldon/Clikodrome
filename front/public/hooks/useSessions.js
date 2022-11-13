import { useEffect, useState } from "preact/hooks";
import { getSessions } from "../api";
import { useAuth } from "../context/auth";

export default function useSessions() {
    const [sessions, setSessions] = useState(undefined)
    const token = useAuth()

    async function fetchSessions() {
        getSessions(token).then((res) => {
            if (res.result) {
                setSessions(res.result.reverse());
            }
        });
    }

    useEffect(() => {
        fetchSessions()
    }, [token]);

    return {sessions, fetchSessions}
}