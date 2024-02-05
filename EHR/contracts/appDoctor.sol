// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;


// 呼び出したいコントラクトの関数が定義されたインターフェース
interface DataContract {
    function getStealth(address conAddr) external returns (string memory);
    function getData(address conAddr) external returns (string[] memory);
}


contract appDoc{
    address public owner;

    // コンストラクターでコントラクトのデプロイアーを所有者として設定
    constructor() {
        owner = msg.sender;
    }

    // 状態変数の定義
    string[] thisEnPermMap;


    function deployAccPerm(address dataConAddr, string memory myStealth, string[] memory EnPermMap) public{
        DataContract data = DataContract(dataConAddr);
        string memory stealthAddr = data.getStealth(dataConAddr);
        if (msg.sender == owner && keccak256(abi.encodePacked(stealthAddr)) == keccak256(abi.encodePacked(myStealth))) {
           thisEnPermMap = EnPermMap;
        }
    }

    function AccPermReq(address addrFromPermMap) public returns(string[] memory){
        if (addrFromPermMap != address(0)){
            DataContract data = DataContract(addrFromPermMap);
            string[] memory ipfsAddr = data.getData(addrFromPermMap);
            return ipfsAddr;
        }
        else{
            return new string[](0); // 空の配列を正しく初期化
        }
    }

    function getEnPermMap(address conAddr) public view returns(string[] memory){
        if (conAddr != address(0)) {
            return thisEnPermMap;
        } else {
            string[] memory emptyArray;
            return emptyArray;
        }

    }
}