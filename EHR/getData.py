from web3 import Web3, HTTPProvider
import ipfshttpclient
from addToIPFS import addToIPFS
import json

def getData(Datacontract_address):
    #web3 = Web3(Web3.HTTPProvider('http://10.34.4.206:7545'))
    web3 = Web3(Web3.HTTPProvider('http://192.168.151.43:7545'))
    print(web3.is_connected())

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
    loadFile = json.load(open('./contractAddress.json'))
    contract_address = loadFile["contractUserAddress"]# コントラクトのアドレス
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    generatorAddr = contract.functions.getSenderAddress().call()#ユーザのアドレス
    print(generatorAddr)

    #IPFSのアドレスを渡す
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
    ] #コントラクトのABI
    contract = web3.eth.contract(address=Datacontract_address, abi=contract_abi)
    
    ipfsAddr = contract.functions.getData(Datacontract_address).call()
    return ipfsAddr

if __name__ == "__main__":
    loadFile = json.load(open('./contractAddress.json'))
    Datacontract_address = loadFile["contractData"]# コントラクトのアドレス
    ipfsAddr = []
    ipfsAddr.extend(getData(Datacontract_address))
    print(ipfsAddr)
    print("append OK")
    # IPFSノードに接続
    client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')  # IPFSノードのアドレスに応じて変更
    for hash in ipfsAddr:
        try:
            content = client.cat(hash)
            print(content)
        except ipfshttpclient.exceptions.ErrorResponse as e:
            if "this dag node is a directory" in str(e):
                print(f"The hash {hash} is a directory, skipping.")
            else:
                raise e
    # クライアント接続を閉じる
    client.close()

    print("OK")
