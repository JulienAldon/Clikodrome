import Cookies from "js-cookie";
import { createContext } from "preact";
import { useState, useContext } from "preact/hooks";

const AuthContext = createContext(null);

function AuthProvider(props) {
    const [token, setToken] = useState(() => Cookies.get('token'));
    return (<AuthContext.Provider value={token}>
        {props.children}
    </AuthContext.Provider>
    );
}

function useAuth() {
    const context = useContext(AuthContext);

    if (AuthContext === undefined) {
        throw new Error ('Context Provider is missing')
    }
    return context;
}

export { useAuth, AuthProvider }