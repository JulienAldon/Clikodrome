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
        getSessions(token).then((res) => {
            if (res.hasOwnProperty('detail')) {
                logout();
            }            
        });

        if (role && intraRole !== role) {
            logout();
        }
    }, [token]);
    return {token, intraRole};
}

export {
    login,
    useAuthGuard
}