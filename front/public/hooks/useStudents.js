import { useEffect, useState } from "preact/hooks";
import { getStudents } from "../api";
import { useAuth } from "../context/auth";

export default function useStudents() {
    const [students, setStudents] = useState(undefined);
    const { token, intraRole} = useAuth()
    
    async function fetchStudents() {
        getStudents(token).then((res) => {
            if (res.result)
                setStudents(res.result)
        })
    }

    useEffect(() => {
        fetchStudents()
    }, [token])

    return {
        students,
        fetchStudents,
    }
}