import { useEffect, useState } from "preact/hooks"
import { useAuth } from "../context/auth";
import { getEdusignGroups } from "../api";

export default function useGroup() {
    const [ groups, setGroups ] = useState([]);
    const { token, intraRole } = useAuth()

    async function fetchEdusignGroup() {
        getEdusignGroups(token).then((data) => {
            setGroups(data)
        });
    }

    useEffect(() => {
        fetchEdusignGroup()
    }, [token])

    useEffect(() => {
    }, [groups]);

    return {
        groups,
        fetchEdusignGroup,
    }
}