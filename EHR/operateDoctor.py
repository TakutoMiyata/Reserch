from HIBE import *
from web3 import Web3, HTTPProvider
import ipfshttpclient
from addToIPFS import addToIPFS
import json
import pickle
from stealthAddr import *

web3 = Web3(Web3.HTTPProvider('http://10.34.4.206:7545'))
#web3 = Web3(Web3.HTTPProvider('http://192.168.151.43:7545'))
#print(web3.is_connected())

loadFile = json.load(open('./contractAddress.json'))
appDoc_address = loadFile["contractAppDoctor"]# コントラクトのアドレス
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
          "name": "dataConAddr",
          "type": "address"
        },
        {
          "internalType": "string",
          "name": "myStealth",
          "type": "string"
        },
        {
          "internalType": "string[]",
          "name": "EnPermMap",
          "type": "string[]"
        }
      ],
      "name": "deployAccPerm",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "addrFromPermMap",
          "type": "address"
        }
      ],
      "name": "AccPermReq",
      "outputs": [
        {
          "internalType": "string[]",
          "name": "",
          "type": "string[]"
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
      "name": "getEnPermMap",
      "outputs": [
        {
          "internalType": "string[]",
          "name": "",
          "type": "string[]"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    }
  ]#appDocのabi
contract = web3.eth.contract(address=appDoc_address, abi=contract_abi)

contract_abi_data = [
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
contract_address_data = loadFile["contractData"]# コントラクトのアドレス
contract_data = web3.eth.contract(address=contract_address_data, abi=contract_abi_data)

def makeEnPermMap(Datacontract_address, hospitalAddr, System_para, PP):
    permMap = (Datacontract_address, hospitalAddr)
    # タプルを文字列に変換し、エンコード
    permMap_str = f"{permMap[0]},{permMap[1]}" # カンマ区切りなどでフォーマット
    permMap_bytes = permMap_str.encode() # utf-8でエンコード
    print("make permMap")
    '''
    for i in range (len(hospitalAddr)):
        Enc_key, enPermMap = Enc(System_para, PP, hospitalAddr[i], permMap)
        EncKey.append(Enc_key)
        enPermMapArray.append(enPermMap)
    '''
    EncKey, enPermMapArray = Enc(System_para, PP, hospitalAddr, permMap_bytes)
    print("I used this address:", hospitalAddr)
    print("make enPermMap")
    return EncKey, enPermMapArray

def decEnPermMap(System_para, PP, Sk, Enc_key, enPermMap):
    permMap_bytes = Dec(System_para, PP, Sk, Enc_key, enPermMap)
    # エンコードされたバイナリデータ（バイト列）から文字列にデコード
    permMap_str_decoded = permMap_bytes.decode('utf-8')
    # 文字列を分割し、タプルに再構成
    permMap_elements = permMap_str_decoded.split(',')
    permMap = (permMap_elements[0], permMap_elements[1])#これで元のpermMapをゲットしたはず

    return permMap

def addEnPermMap(dataConAddr, ADDR, R, USK, P, enPermMap, generate_address):
    myStealth = recoverAddr(ADDR,R,USK,P)
    #print("recover stealth address")
    myStealth = convert_addr_to_string(myStealth)
    contract.functions.deployAccPerm(dataConAddr, myStealth, enPermMap).transact({"from": generate_address})

def getEnPermMap():
    print(web3.is_connected())
    enPermMap = contract.functions.getEnPermMap(appDoc_address).call()
    if enPermMap is not None:
        print("get enPermMap")
    else:
        print("NOT get enPermMap")
    #print(enPermMap)
    return enPermMap
    
def getIPFSaddr(conAddr):
    print(web3.is_connected())
    ipfsAddr = contract_data.functions.getData(conAddr).call()

    return ipfsAddr

def checkStealth(ADDR,R,USK,P):
    getStealthAddr = contract_data.functions.getStealth(contract_address_data).call()
    stealthAddr = recoverAddr(ADDR,R,USK,P)
    stealthAddr = convert_addr_to_string(stealthAddr)
    if getStealthAddr == stealthAddr:
        print("stealthAddr OK")
    else:
        print("miss")
        print("getStealthAddr",getStealthAddr)
        print("stealthAddr",stealthAddr)
