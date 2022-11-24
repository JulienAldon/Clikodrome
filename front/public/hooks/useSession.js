import { useEffect, useState } from "preact/hooks"
import { getSession } from "../api";
import { useAuth } from "../context/auth";

export default function useSession(id) {
    const [session, setSession] = useState(undefined);
    const [students, setStudents] = useState(undefined);
    const token = useAuth()

    async function fetchSession() {
        getSession(token, id).then((res) => {
            setStudents(res.students);
            setSession(res.session);
        })
    }

    useEffect(() => {
        fetchSession()
    }, [token])

    return {
        students,
        session,
        fetchSession,
        setStudents,
    }
}