import React, { useState } from 'react';
import './AddressInput.css';

export default function AddressInput({
    value,
    onChange,
    placeholder = 'Введите адрес контракта',
    disabled = false,
}) {
    const [error, setError] = useState('');
    const [focused, setFocused] = useState(false);

    const validate = (inputValue) => {
        if (!/^0x[a-fA-F0-9]{0,40}$/.test(inputValue)) {
            if (inputValue.length === 0) return '';
            if (!inputValue.startsWith('0x')) return 'Адрес должен начинаться с "0x"';
            if (inputValue.length !== 42) return 'Ethereum-адрес должен содержать 42 символа';
            return 'Адрес содержит недопустимые символы';
        } else if (inputValue.length === 42) {
            return '';
        } else {
            return 'Ethereum-адрес должен содержать 42 символа';
        }
    };

    const handleChange = (e) => {
        const inputValue = e.target.value;
        onChange(inputValue);

        const validationError = validate(inputValue);
        setError(validationError);
    };

    const handleFocus = () => setFocused(true);
    const handleBlur = () => setFocused(false);

    const isValid = value && error === '';
    const showError = error !== '';

    return (
        <div className="inputContainer">
            <label className="label">Адрес смарт-контракта</label>
            <input
                type="text"
                value={value}
                onChange={handleChange}
                onFocus={handleFocus}
                onBlur={handleBlur}
                placeholder={placeholder}
                disabled={disabled}
                className={`input
                    ${isValid ? 'inputValid' : ''}
                    ${showError && !focused ? 'inputError' : ''}
                `}
            />
            {showError && (
                <span className={`error ${focused ? 'errorGray' : 'errorRed'}`}>
                    {error}
                </span>
            )}
        </div>
    );
}