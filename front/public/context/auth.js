import Cookies from "js-cookie";
import { createContext } from "preact";
import { useState, useContext, useEffect } from "preact/hooks";
import { jwtDecode } from "jwt-decode";
import { logout } from "./useUser";

const AuthContext = createContext(null);

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
        let decodedToken = jwtDecode(token);
        let currentDate = new Date();
        console.log(token, intraRole);
        if (decodedToken.exp * 1000 < currentDate.getTime()) {
            logout();
            console.log('logout because token was expired')
        }
    }, [token])

    if (AuthContext === undefined) {
        throw new Error ('Context Provider is missing')
    }
    return {token, intraRole};
}

export { useAuth, AuthProvider }