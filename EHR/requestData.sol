// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IDataContract {
    function getData(address conAddr) external view returns (string memory);
}

contract requestData{
    // アクセス権限のデプロイ
    function deployAccPerm(address dataConAddr, bytes memory enPermMap, bytes memory enSymKey) public returns (address) {
        if (msg.sender == dataConAddr) {
            // ここに権限マップと対称鍵を保存するロジックを追加
            return address(this);
        } else {
            return address(0);
        }
    }

    // 権限要求
    function accPermReq(address conAddr) public returns (string memory) {
        // ここに暗号化解除のロジックを追加
        // 例えば、decrypt(enSymKey, sk) != null
        if (true) { // 仮の条件
            // ここにデータ取得と返却のロジックを追加
            IDataContract dataContract = IDataContract(conAddr);
            string memory IPFSaddr = dataContract.getData(conAddr);
            return IPFSaddr; // 例えば、IPFS(IPFSaddr)を返す
        } else {
            return "";
        }
    }
}