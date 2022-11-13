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
	window.location.replace(`${settings.ORIGIN}/`);
}

export default function useAuthGuard() {
    const token = useAuth();
    useEffect(() => {
        getSessions(token).then((res) => {
            if (res.hasOwnProperty('detail')) {
                Cookies.remove('token');
                window.location.replace(`${settings.ORIGIN}/`)
            }            
        });
    }, []);
    return token
}

export {
    login,
    logout,
    useAuthGuard
}