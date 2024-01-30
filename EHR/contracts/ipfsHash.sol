// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract IPFSStorage {
    // IPFSファイルのハッシュを格納する変数
    string public ipfsHash;

    // イベントの宣言
    event HashStored(string _ipfsHash);

    // ハッシュを保存する関数
    function setHash(string memory _ipfsHash) public {
        ipfsHash = _ipfsHash;
        emit HashStored(_ipfsHash);
    }

    // ハッシュを取得する関数
    function getHash() public view returns (string memory) {
        return ipfsHash;
    }
}
