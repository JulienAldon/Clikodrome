import { useAuth, logout } from "./auth";
import { getSessions } from "../api";
import { useEffect } from "preact/hooks";
import settings from "../settings";

function login() {
	window.location.replace(`${settings.SERVICE_URL}/auth/azure`);
}

export default function useAuthGuard(role) {
    const {token, intraRole} = useAuth();

    useEffect(() => {
        if (role && intraRole !== role || token === undefined) {
            logout();
        }
        getSessions(token).then((res) => {
            if (res.hasOwnProperty('detail')) {
                logout();
            }            
        });
    }, [token]);
    return {token, intraRole};
}

export {
    login,
    useAuthGuard
}