// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract UserAddress {
    // この関数はトランザクションを送信したユーザのアドレスを返します
    function getSenderAddress() public view returns (address) {
        return msg.sender;
    }
}
