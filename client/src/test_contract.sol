// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MyContract {
    // Хранение значения (переменная типа uint256)
    uint256 public storedValue;

    // Событие, которое будет генерироваться при изменении значения
    event ValueChanged(uint256 newValue);

    // Конструктор, который инициализирует контракт с начальным значением
    constructor(uint256 initialValue) {
        storedValue = initialValue;
    }

    // Функция для установки нового значения
    function setValue(uint256 newValue) public {
        storedValue = newValue;
        emit ValueChanged(newValue); // Генерируем событие при изменении значения
    }

    // Функция для получения текущего значения
    function getValue() public view returns (uint256) {
        return storedValue;
    }
}
