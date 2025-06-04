// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Proxy {
    address public implementation;
    address public owner;

    constructor(address _impl) {
        implementation = _impl;
        owner = msg.sender;
    }

    function updateImplementation(address _newImpl) external {
        require(msg.sender == owner, "Only owner");
        implementation = _newImpl;
    }

    fallback() external payable {
        // delegate all calls
        (bool success, ) = implementation.delegatecall(msg.data);
        require(success, "Delegatecall failed");
    }
}
