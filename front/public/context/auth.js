import Cookies from "js-cookie";
import { createContext } from "preact";
import { useState, useContext, useEffect } from "preact/hooks";
import { jwtDecode } from "jwt-decode";
import settings from '../settings';

const AuthContext = createContext(null);

function logout() {
    Cookies.remove('token');
    Cookies.remove('role');
    Cookies.remove('user');
    window.location.replace(`${settings.ORIGIN}/`)
}

function AuthProvider(props) {
    const [token, setToken] = useState(() => Cookies.get('token'));
    const [intraRole, setIntraRole] = useState(() => Cookies.get('role'));
    return (<AuthContext.Provider value={{token, intraRole}}>
        {props.children}
    </AuthContext.Provider>
    );
}

function useAuth() {
    const {token, intraRole} = useContext(AuthContext);

    useEffect(() => {
        if (token === undefined) {
            return
        }
        let decodedToken = jwtDecode(token);
        let currentDate = new Date();
        if (decodedToken.exp * 1000 < currentDate.getTime()) {
            console.log('logout because token was expired')
            logout();
        }
    }, [token])

    return {token, intraRole};
}

export { useAuth, AuthProvider, logout }