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
    uint[] thisEnPermMap;


    function deployAccPerm(address dataConAddr, string memory myStealth, uint[] memory EnPermMap) public {
        DataContract data = DataContract(dataConAddr);
        string memory stealthAddr = data.getStealth(dataConAddr);
        if (msg.sender == owner && keccak256(abi.encodePacked(stealthAddr)) == keccak256(abi.encodePacked(myStealth))) {
           thisEnPermMap = EnPermMap;
        }
    }

    function AccPermReq(uint PermMap) public returns(string[] memory){
        if (PermMap != 0){
            address conAddr = address(uint160(PermMap));  //型を変換する．
            DataContract data = DataContract(conAddr);
            string[] memory IPFSaddr = data.getData(conAddr);
            return IPFSaddr;
        }
        else{
            return new string[](0); // 空の配列を正しく初期化
        }
    }

    function getEnPermMap(address conAddr) public view returns(uint[] memory){
        if (conAddr != address(0)) {
            return thisEnPermMap;
        } else {
            uint[] memory emptyArray;
            return emptyArray;
        }

    }
}