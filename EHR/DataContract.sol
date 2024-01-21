// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DataContract{
    address public owner;

    // コンストラクターでコントラクトのデプロイアーを所有者として設定
    constructor() {
        owner = msg.sender;
    }

    // データ構造の定義
    struct Record {
        string SA;
        string IPFSaddr;
        string sign;
    }

    // レコードの保存
    mapping(address => Record) public records;

    // この関数は所有者によってのみ呼び出すことができる
    // データの追加
    function addData(string memory SA, string memory IPFSaddr, string memory sign, address from) public returns (bool) {
        if (msg.sender == from) {
            records[from] = Record(SA, IPFSaddr, sign);
            return true;
        } else {
            
            return false;
        }
    }

    // データの取得
    function getData(address conAddr) public view returns (string memory) {
        if (conAddr != address(0)) {
            return records[conAddr].IPFSaddr;
        } else {
            return "";
        }
    }
    

}