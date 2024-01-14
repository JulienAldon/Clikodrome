import { useEffect, useState } from "preact/hooks"
import { getSession, getSessionSignatures } from "../api";
import { useAuth } from "../context/auth";

export default function useSession(id) {
    const [session, setSession] = useState(undefined);
    const [students, setStudents] = useState(undefined);
    const [signLinks, setsignLinks] = useState(undefined);
    const [signatureLinkLoader, setSignatureLinkLoader] = useState(false);
    const { token, intraRole} = useAuth()

    async function fetchSession() {
        getSession(token, id).then((res) => {
            if (res.session.length === 0) {
                setSession(undefined);
                setStudents(undefined);
            } else {
                setStudents(res.students);
                setSession(res.session);
                fetchSignatureLink()
            }
        })
    }

    async function fetchSignatureLink() {
        setSignatureLinkLoader(true);
        getSessionSignatures(token, id).then((res) => {
            setsignLinks(res);
            setSignatureLinkLoader(false);
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
        signLinks,
        fetchSignatureLink,
        signatureLinkLoader
    }
}