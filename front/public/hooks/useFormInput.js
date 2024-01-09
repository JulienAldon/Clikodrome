import { useState } from "preact/hooks";

export default function useFormInput() {
    const [ formValue, setFormValue ] = useState(null);

    const resetFormValue = () => {
        setFormValue(null);
    }

    const handleFormChange = (event) => {
        setFormValue(event.target.value);
    }

    return {
        value: formValue,
        onChange: handleFormChange,
        resetFormValue: resetFormValue
    }
}