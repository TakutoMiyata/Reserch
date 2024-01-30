# 1. Import Module
import json
from web3 import Web3, HTTPProvider

def deploy(seed):
    if (seed==0):
        # 2. Access Ganache local server
        settingFile = json.load(open('./setting.json'))
        # HTTP通信用URL読み込み
        url = settingFile['url']
        web3 = Web3(HTTPProvider(url))
        print(web3.is_connected())

        # 3. private key
        # accountのprivate key読み込み
        key = settingFile['privateKey']
        acct = web3.eth.account.from_key(key)

        # abi，bytecodeを読み込む
        #truffleFile = json.load(open('./build/contracts/deployしたいファイル名.json'))
        truffleFile = json.load(open('./build/contracts/DataContract.json'))
        #truffleFile = json.load(open('./build/contracts/UserAddress.json'))

        abi = truffleFile['abi']
        bytecode = truffleFile['bytecode']
        contract= web3.eth.contract(bytecode=bytecode, abi=abi)

        # 5. Building transaction information
        # コントラクトのGASなどの設定を行う
        construct_txn = contract.constructor().build_transaction({
            'from': acct.address,
            'nonce': web3.eth.get_transaction_count(acct.address),
            'gas': 3000000,
            'gasPrice': web3.to_wei('21', 'gwei')})

        # 6. Send Transaction
        # コントラクトをデプロイ
        signed = acct.sign_transaction(construct_txn)
        tx_hash = web3.eth.send_raw_transaction(signed.rawTransaction)
        print(tx_hash.hex())

        # 7. Display contract address
        # コントラクトアドレスなどを表示した後，jsonファイルにも保存
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        print("Contract Deployed At:", tx_receipt['contractAddress'])

        with open('./contractAddress.json') as f:
            update = json.load(f)

        #update['デプロイしたファイルを示す言葉'] = tx_receipt['contractAddress']
        update['contractData'] = tx_receipt['contractAddress']
        #update['contractUserAddress'] = tx_receipt['contractAddress']


        with open('./contractAddress.json', 'w') as f:
            json.dump(update, f, indent=2)
    if (seed==1):
        # 2. Access Ganache local server
        settingFile = json.load(open('./setting.json'))
        # HTTP通信用URL読み込み
        url = settingFile['url']
        web3 = Web3(HTTPProvider(url))
        print(web3.is_connected())

        # 3. private key
        # accountのprivate key読み込み
        key = settingFile['privateKey']
        acct = web3.eth.account.from_key(key)

        # abi，bytecodeを読み込む
        #truffleFile = json.load(open('./build/contracts/deployしたいファイル名.json'))
        #truffleFile = json.load(open('./build/contracts/DataContract.json'))
        truffleFile = json.load(open('./build/contracts/UserAddress.json'))

        abi = truffleFile['abi']
        bytecode = truffleFile['bytecode']
        contract= web3.eth.contract(bytecode=bytecode, abi=abi)

        # 5. Building transaction information
        # コントラクトのGASなどの設定を行う
        construct_txn = contract.constructor().build_transaction({
            'from': acct.address,
            'nonce': web3.eth.get_transaction_count(acct.address),
            'gas': 3000000,
            'gasPrice': web3.to_wei('21', 'gwei')})

        # 6. Send Transaction
        # コントラクトをデプロイ
        signed = acct.sign_transaction(construct_txn)
        tx_hash = web3.eth.send_raw_transaction(signed.rawTransaction)
        print(tx_hash.hex())

        # 7. Display contract address
        # コントラクトアドレスなどを表示した後，jsonファイルにも保存
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        print("Contract Deployed At:", tx_receipt['contractAddress'])

        with open('./contractAddress.json') as f:
            update = json.load(f)

        #update['デプロイしたファイルを示す言葉'] = tx_receipt['contractAddress']
        update['contractUserAddress'] = tx_receipt['contractAddress']
        #update['contractUserAddress'] = tx_receipt['contractAddress']


        with open('./contractAddress.json', 'w') as f:
            json.dump(update, f, indent=2)

if __name__ == "__main__":
    deploy(0)
    deploy(1)
    print("finish")
