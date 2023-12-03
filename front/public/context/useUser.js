import { useAuth } from "./auth";
import Cookies from 'js-cookie';
import { getSessions } from "../api";
import settings from '../settings';
import { useEffect } from "preact/hooks";

function login() {
	window.location.replace(`${settings.SERVICE_URL}/auth/azure`);
}

function logout() {
    Cookies.remove('token');
    Cookies.remove('intra-role');
    Cookies.remove('user');
    window.location.replace(`${settings.ORIGIN}/`)
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
    logout,
    useAuthGuard
}