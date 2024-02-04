from web3 import Web3, HTTPProvider
import ipfshttpclient
from addToIPFS import addToIPFS
import json


def getData(Datacontract_address):
    web3 = Web3(Web3.HTTPProvider('http://10.34.4.206:7545'))
    #web3 = Web3(Web3.HTTPProvider('http://192.168.151.43:7545'))
    print(web3.is_connected())

    # IPFSノードに接続
    client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')  # IPFSノードのアドレスに応じて変更
    '''
    for hash in ipfsAddr:
        try:
            content = client.cat(hash)
            data = pickle.loads(content)
            msg = Dec(System_para, PP, Sk_ID1, Enc_key, data)
            print(content)
        except ipfshttpclient.exceptions.ErrorResponse as e:
            if "this dag node is a directory" in str(e):
                print(f"The hash {hash} is a directory, skipping.")
            else:
                raise e
    '''
    content = client.cat(ipfsAddr[0])
    data = pickle.loads(content)
    msg = Dec(System_para, PP, Sk_ID, EncKey, data)
    print(content)

    # クライアント接続を閉じる
    client.close()


