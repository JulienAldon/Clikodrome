import { createContext } from "preact";
import { useContext, useEffect, useState } from "preact/hooks";

export const ToastContext = createContext(null);

export const useToast = () => useContext(ToastContext);

export const ToastProvider = ({ children }) => {
    const [ toastList, setToastList ] = useState([]);
    
    // XXX: Probably bugged submit to further testing 
    useEffect(() => {
        if (toastList.length > 1) {
            toastList.shift();
            setToastList([...toastList])
        }
    }, toastList)

    return (
        <ToastContext.Provider value={{ toastList, setToastList}}>
            { children }
        </ToastContext.Provider>
    );
};