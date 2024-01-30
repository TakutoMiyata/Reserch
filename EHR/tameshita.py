from web3 import Web3, HTTPProvider
import json

def tameshita():
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


if __name__ == "__main__":
    tameshita()
