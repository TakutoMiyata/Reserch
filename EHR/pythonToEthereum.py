from web3 import Web3

account_1 = '0xe22694a13837DA6bC13B666b37A5Cb321B654b49'
account_2 = '0x86271bdb5f5D09985fdf61e6b107946F19D9d84C'
account_3 = '0xF3e6D50C05a4C3c2B4e016a9eEBeAd7610fcf64A'

private_key_1 = '0xbca0982101ca6a6eb13469795d5349b3a766e3a9cd4fa3e3c773a53fd305feb0'
private_key_2 = '0xa8f7de0ee570a9b5d8dbff937300cec0cc027a9ea5741df7de64fb39dbae64f6'
private_key_3 = '0x0b200f0ba7b989adf22cfd144c856cc468a6f24dd8acb1b25bbac7b33ecef07e'

# Ganacheに接続する
w3 = Web3(Web3.HTTPProvider('http://10.34.4.206:7545'))
print(w3.isConnected())

# スマートコントラクトのABIとアドレス
contract_address = ''

abi = [
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
          "internalType": "string",
          "name": "IPFSaddr",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "sign",
          "type": "string"
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
          "internalType": "string",
          "name": "IPFSaddr",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "sign",
          "type": "string"
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
          "internalType": "string",
          "name": "",
          "type": "string"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    }
  ],

# コントラクトのインスタンス生成
contract = w3.eth.contract(address=contract_address, abi=abi)

'''
# addData関数を呼び出し
tx_hash = contract.functions.addData(
    'サンプルSA',
    'サンプルIPFSアドレス',
    'サンプル署名',
    '0xあなたのアドレス'
).transact({'from': w3.eth.accounts[0]})

# トランザクションの結果を待機
receipt = w3.eth.waitForTransactionReceipt(tx_hash)

# getData関数を呼び出し
ipfs_address = contract.functions.getData('0xあなたのアドレス').call()
print(ipfs_address)
'''
print("access OK")
