from web3 import Web3, HTTPProvider
import ipfshttpclient
from addToIPFS import addToIPFS
import json
from stealthAddr import *
from addData import addData
from getData import getData
import os
from HIBE import *
import pickle
from writeToFile import encAndWrite
from operateDoctor import *


if __name__ == "__main__":
    seed = 0 #患者が自分のデータを登録，確認する場合．
    seed = 1 #患者がデータを登録し，病院側がデータを閲覧する場合．

    #seed0 患者が自分のデータを登録，確認する場合．
    #------------------------------------------------------------------------------------
    if seed == 0:
        System_para, PP, ID, Sk_ID, EncKey = encAndWrite()#ファイルに書き込み

        addData("otameshiFolder")#ファイルをIPFSに乗っける

        loadFile = json.load(open('./contractAddress.json'))
        Datacontract_address = loadFile["contractData"]# コントラクトのアドレス
        ipfsAddr = []
        ipfsAddr.extend(getData(Datacontract_address))
        print(ipfsAddr)
        print("append OK")
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
        content = client.cat(ipfsAddr[2])
        data = pickle.loads(content)
        msg = Dec(System_para, PP, Sk_ID[0], EncKey[0], data)#バイナリ形式で帰ってくる
        print(msg)
        # クライアント接続を閉じる
        client.close()
    #------------------------------------------------------------------------------------
    
    
    #seed1 患者がデータを登録し，病院側がデータを閲覧する場合．
    #------------------------------------------------------------------------------------
    if seed == 1:
        System_para, PP, ID, Sk_ID, EncKey = encAndWrite()#ファイルに書き込み
        addData("otameshiFolder")#ファイルをIPFSに乗っける
    #データの登録完了
    #------------------------------------------------------------------------------------
        loadFile = json.load(open('./contractAddress.json'))
        Datacontract_address = loadFile["contractData"]# コントラクトのアドレス
        hospitalAddr = ["0xd691b959f1624B4b721e58a6DcEf363fEDA1D4F1","0xD3C6d21cdCAA34EcFb5A2ca57C9096506ed88131", "0x67c9268ded4162756429Fef09c7D673Efd906Dd1"] #許可する病院のアドレス
        Enc_key, enPermMap = makeEnPermMap(Datacontract_address, hospitalAddr, System_para, PP)

    #病院を登録
    #------------------------------------------------------------------------------------
        #appDoctor.solからenPermMapをゲットする．
        enPermMap = getEnPermMap
        permMap = decEnPermMap(System_para, PP, Sk_ID[0], Enc_key[0], enPermMap[0])
        dataConAddr = permMap[0]
