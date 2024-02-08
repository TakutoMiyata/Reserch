from web3 import Web3, HTTPProvider
import ipfshttpclient
from addToIPFS_fileNumber import addToIPFS
import json
from stealthAddr import *

def addData(folderName):
    # IPFSにデータを追加
    ehrAddr, names = addToIPFS(folderName)
    print("add to IPFS")

    # ステルスアドレスを計算
    web3 = Web3(Web3.HTTPProvider('http://10.34.4.206:7545'))
    #web3 = Web3(Web3.HTTPProvider('http://192.168.151.43:7545'))
    settingFile = json.load(open('./setting.json'))
    key = settingFile['privateKey']
    acct = web3.eth.account.from_key(key)
    id = acct.address
    print("ID:",id)
    
    P = 10
    msk, MPK = setup(P)
    id_encode = id.encode('utf-8')
    UPK, USK = keyGen(id_encode, MPK, P)
    stealthAddr = 0
    stealthAddr, R = generate_address_for_id(id, P)
    stealthAddr = convert_addr_to_string(stealthAddr)

    print("compute Stealh Address")
    print("stealth Address:",stealthAddr)

    # (EHR addr, ステルスアドレス, generator's addr)をconstoractorでブロックチェーンに保存
    '''
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
    #print(generatorAddr)
    '''
    # DataContract.solを呼び出してdataをブロックチェーンに保存
    contract_abi = [
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
          "internalType": "string[]",
          "name": "IPFSaddr",
          "type": "string[]"
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
          "internalType": "string[]",
          "name": "",
          "type": "string[]"
        }
      ],
      "stateMutability": "view",
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
      "name": "getStealth",
      "outputs": [
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    }
  ]
    #コントラクトのABI
    loadFile = json.load(open('./contractAddress.json'))    # コントラクトのアドレス
    contract_address = loadFile["contractData"]# コントラクトのアドレス
    print("contract address: " + contract_address)

    contract = web3.eth.contract(address=contract_address, abi=contract_abi)
    generatorAddr = id
    #本当は上で呼び出したアドレスがgeneratoeAddrなんか上手くいかん
    contract.functions.addData(stealthAddr, ehrAddr, generatorAddr).transact({'from': generatorAddr})
    print("store to blockchain")
    return stealthAddr, USK, R, P, names

if __name__ == "__main__":
    addData("otameshiFolder")
    print("OK")


