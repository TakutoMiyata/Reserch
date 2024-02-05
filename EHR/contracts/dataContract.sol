// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract data{
    address public owner;

    // コンストラクターでコントラクトのデプロイアーを所有者として設定
    constructor() {
        owner = msg.sender;
    }

    // データ構造の定義
    struct Record {
        string SA;
        string[] IPFSaddr;
        address from;
    }

    // レコードの保存
    mapping(address => Record) public records;

    // この関数は所有者によってのみ呼び出すことができる
    // データの追加
    function addData(string memory SA, string[] memory IPFSaddr, address from) public returns (bool) {
        if (msg.sender == owner) {
            records[address(this)] = Record(SA, IPFSaddr, from);
            return true;
        } else {
            
            return false;
        }
    }

    // データの取得
    function getData(address conAddr) public view returns (string[] memory) {
        if (conAddr != address(0)) {
            return records[conAddr].IPFSaddr;
        } else {
            string[] memory emptyArray;
            return emptyArray;
        }
    }
    
    //stealth addressを返す
    function getStealth(address conAddr) public view returns (string memory){
        if (conAddr != address(0)) {
            return records[conAddr].SA;
        } else {
            return "";
        }

    }
}