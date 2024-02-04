from HIBE import *
from web3 import Web3, HTTPProvider
import ipfshttpclient
from addToIPFS import addToIPFS
import json
import pickle


def makeEnPermMap(Datacontract_address, hospitalAddr, System_para, PP):
    permMap = (Datacontract_address, hospitalAddr)
    for i in range (len(hospitalAddr)):
        Enc_key, enPermMap = Enc(System_para, PP, hospitalAddr[i], permMap)
        EncKey.append(Enc_key)
        enPermMapArray.append(enPermMap)
    return EncKey, enPermMapArray

def decEnPermMap(System_para, PP, Sk, Enc_key, enPermMap):
    permMap = Dec(System_para, PP, Sk, Enc_key, enPermMap)
    return permMap

def getEnPermMap():
    web3 = Web3(Web3.HTTPProvider('http://10.34.4.206:7545'))
    #web3 = Web3(Web3.HTTPProvider('http://192.168.151.43:7545'))
    print(web3.is_connected())

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
      "name": "hospitalData",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "EnSymKey",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
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
          "internalType": "uint256[]",
          "name": "EnPermMap",
          "type": "uint256[]"
        },
        {
          "internalType": "uint256",
          "name": "EnSymKey",
          "type": "uint256"
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
          "internalType": "uint256",
          "name": "PermMap",
          "type": "uint256"
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
    }
  ]#appDocのabi
    contract = web3.eth.contract(address=appDoc_address, abi=contract_abi)
    EnPermMap = contract.getEnPermMap(appDoc_address).call()

def getIPFSaddr():
    web3 = Web3(Web3.HTTPProvider('http://10.34.4.206:7545'))
    #web3 = Web3(Web3.HTTPProvider('http://192.168.151.43:7545'))
    print(web3.is_connected())

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
      "name": "hospitalData",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "EnSymKey",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
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
          "internalType": "uint256[]",
          "name": "EnPermMap",
          "type": "uint256[]"
        },
        {
          "internalType": "uint256",
          "name": "EnSymKey",
          "type": "uint256"
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
          "internalType": "uint256",
          "name": "PermMap",
          "type": "uint256"
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
    }
  ]#appDocのabi
    contract = web3.eth.contract(address=appDoc_address, abi=contract_abi)
