from web3 import Web3, HTTPProvider
import ipfshttpclient
from addToIPFS import addToIPFS
import json


def addData(folderName):
    # IPFSにデータを追加
    ehrAddr = addToIPFS(folderName)
    print("add to IPFS")

    # ステルスアドレスを計算
    #web3 = Web3(Web3.HTTPProvider('http://10.34.4.206:7545'))
    web3 = Web3(Web3.HTTPProvider('http://192.168.151.43:7545'))
    settingFile = json.load(open('./setting.json'))
    key = settingFile['privateKey']
    acct = web3.eth.account.from_key(key)
    print(acct.address)
    
    steathAddr = "0xe22694a13837DA6bC13B666b37A5Cb321B654b49"
    print("compute Stealh Address")
    print(steathAddr)

    # (EHR addr, ステルスアドレス, generator's addr)をconstoractorでブロックチェーンに保存

    # UserAddress.solを呼び出してgenerator's addrを出す
    contract_abi = [
    {
      "inputs": [],
      "name": "getSenderAddress",
      "outputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    }
  ] # コントラクトのABI
    loadFile = json.load(open('./contractAddress.json'))    # コントラクトのアドレス

    contract_address = loadFile["contractUserAddress"]
    print("contract address: " + contract_address)

    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    generatorAddr = contract.functions.getSenderAddress().call()
    print(generatorAddr)

    # DataContract.solを呼び出してdataをブロックチェーンに保存
    contract_abi =  [
    {
      "inputs": [],
      "stateMutability": "nonpayable",
      "type": "constructor"
    },
    {
      "inputs": [],
      "name": "owner",
      "outputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "name": "records",
      "outputs": [
        {
          "internalType": "string",
          "name": "SA",
          "type": "string"
        },
        {
          "internalType": "address",
          "name": "from",
          "type": "address"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "SA",
          "type": "string"
        },
        {
          "internalType": "string[10]",
          "name": "IPFSaddr",
          "type": "string[10]"
        },
        {
          "internalType": "address",
          "name": "from",
          "type": "address"
        }
      ],
      "name": "addData",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "conAddr",
          "type": "address"
        }
      ],
      "name": "getData",
      "outputs": [
        {
          "internalType": "string[10]",
          "name": "",
          "type": "string[10]"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    }
  ]#コントラクトのABI
    contract_address = loadFile["contractData"]# コントラクトのアドレス
    print("contract address: " + contract_address)

    contract = web3.eth.contract(address=contract_address, abi=contract_abi)
    generatorAddr = "0xe22694a13837DA6bC13B666b37A5Cb321B654b49"
    #本当は上で呼び出したアドレスがgeneratoeAddrなんか上手くいかん
    contract.functions.addData(steathAddr, ehrAddr, generatorAddr).transact({'from': generatorAddr})
    print("store to blockchain")

if __name__ == "__main__":
    addData("otameshiFolder")
    print("OK")


