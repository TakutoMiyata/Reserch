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
import time

if __name__ == "__main__":
    #seed = 0 #患者が自分のデータを登録，確認する場合．
    seed = 1 #患者がデータを登録し，病院側がデータを閲覧する場合．

    #seed0 患者が自分のデータを登録，確認する場合．
    #------------------------------------------------------------------------------------
    if seed == 0:
        max_level = 5

        start1 = time.time()
        System_para, PP, MK = Setup(max_level)
        end1 = time.time()
        SetupTime = (end1 - start1)*1000

        ID=[]
        ID.append(["0xd691b959f1624B4b721e58a6DcEf363fEDA1D4F1"])#ブロックチェーンのアドレス
        ID.append(["0xd691b959f1624B4b721e58a6DcEf363fEDA1D4F1","0xD3C6d21cdCAA34EcFb5A2ca57C9096506ed88131"])
        ID.append(["0xd691b959f1624B4b721e58a6DcEf363fEDA1D4F1", "0xD3C6d21cdCAA34EcFb5A2ca57C9096506ed88131", "0x67c9268ded4162756429Fef09c7D673Efd906Dd1"])

        Sk_ID, EncKey, SkGenTime, EncTime = encAndWrite(System_para, PP, MK, ID)#ファイルに書き込み

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

        start4 = time.time()
        msg = Dec(System_para, PP, Sk_ID[0], EncKey[0], data)#バイナリ形式で帰ってくる
        end4 = time.time()
        DecTime = (end4 - start4)*1000

        print(msg)
        # クライアント接続を閉じる
        client.close()
        print("Setup:%f ms" % SetupTime)
        print("SkGen:%f ms" % SkGenTime)
        print("Enc:%f ms" % EncTime)
        print("Dec:%f ms" % DecTime)
    #------------------------------------------------------------------------------------
    
    
    #seed1 患者がデータを登録し，病院側がデータを閲覧する場合．
    #------------------------------------------------------------------------------------
    if seed == 1:
        max_level = 5

        start1 = time.time()
        System_para, PP, MK = Setup(max_level)
        end1 = time.time()
        SetupTime = (end1 - start1)*1000
        
        ID=[]
        ID.append(["0xd691b959f1624B4b721e58a6DcEf363fEDA1D4F1"])
        ID.append(["0xd691b959f1624B4b721e58a6DcEf363fEDA1D4F1","0xD3C6d21cdCAA34EcFb5A2ca57C9096506ed88131"])
        ID.append(["0xd691b959f1624B4b721e58a6DcEf363fEDA1D4F1", "0xD3C6d21cdCAA34EcFb5A2ca57C9096506ed88131", "0x67c9268ded4162756429Fef09c7D673Efd906Dd1"])

        start_upload = time.time()
        
        Sk_ID, EncKey, SkGenTime, EncTime = encAndWrite(System_para, PP, MK, ID)#ファイルに書き込み
        stealthAddr, USK, R, P = addData("otameshiFolder")#ファイルをIPFSに乗っける
        print("データの登録を完了しました")

        end_upload = time.time()
        time_upload = (end_upload - start_upload)*1000
    #データの登録完了
    #------------------------------------------------------------------------------------
        loadFile = json.load(open('./contractAddress.json'))
        Datacontract_address = loadFile["contractData"]# コントラクトのアドレス
        hospitalAddr = []
        #hospitalAddr = ["0xd691b959f1624B4b721e58a6DcEf363fEDA1D4F1","0xD3C6d21cdCAA34EcFb5A2ca57C9096506ed88131", "0x67c9268ded4162756429Fef09c7D673Efd906Dd1"] #許可する病院のアドレス
        hospitalAddr.append(["0xd691b959f1624B4b721e58a6DcEf363fEDA1D4F1"])
        print("hospitalAddr:", hospitalAddr)

        Enc_key, enPermMap = makeEnPermMap(Datacontract_address, hospitalAddr, System_para, PP)
        #print("enPermMap:", enPermMap) 
        enPermMap = list(enPermMap.values())
        #print("enPermMap:", enPermMap)

        settingFile = json.load(open('./setting.json'))
        key = settingFile['privateKey']
        acct = web3.eth.account.from_key(key)
        generate_address = acct.address
        print("stealth addr:",stealthAddr)
        checkStealth(stealthAddr,R,USK,P)#check
        addEnPermMap(Datacontract_address, stealthAddr, R, USK, P, enPermMap, "0xd691b959f1624B4b721e58a6DcEf363fEDA1D4F1")
        print("病院の登録を完了しました")
    #病院を登録
    #------------------------------------------------------------------------------------
        #appDoctor.solからenPermMapをゲットする．
        start_getData = time.time()

        doc_enPermMap=[]
        doc_enPermMap.extend(getEnPermMap())
        #if doc_enPermMap is None:
        #   print("NOT get doc_enPermMap")
        if doc_enPermMap == enPermMap:
            print("enPermMap OK")
        else:
            print("enPermMap miss")
            print("enPermMap:", enPermMap)
            print("doc_enPermMap:", doc_enPermMap)

        # 元の辞書のキー
        keys = ['alg', 'msg', 'digest']
        # 辞書の再構築
        doc_enPermMap = dict(zip(keys, doc_enPermMap))
        #print("doc_enPermMp",doc_enPermMap)

        permMap = decEnPermMap(System_para, PP, Sk_ID[0], Enc_key, doc_enPermMap)
        print(permMap)

        ipfsAddr = []
        ipfsAddr.extend(getIPFSaddr(permMap[0]))
        print(ipfsAddr)
        print("append OK")

        # IPFSノードに接続
        client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')  # IPFSノードのアドレスに応じて変更

        content = []
        content.append(client.cat(ipfsAddr[2]))
        content.append(client.cat(ipfsAddr[1]))
        content.append(client.cat(ipfsAddr[0]))
        content.append(client.cat(ipfsAddr[3]))
        content.append(client.cat(ipfsAddr[4]))
        content.append(client.cat(ipfsAddr[6]))
        content.append(client.cat(ipfsAddr[5]))

        data = []
        for i in range(len(content)):   
            data.append(pickle.loads(content[i]))

        msg = []
        start4 = time.time()
        msg.append(Dec(System_para, PP, Sk_ID[0], EncKey[0], data[0]))#バイナリ形式で帰ってくる
        msg.append(Dec(System_para, PP, Sk_ID[0], EncKey[1], data[1]))
        msg.append(Dec(System_para, PP, Sk_ID[0], EncKey[2], data[2]))
        msg.append(Dec(System_para, PP, Sk_ID[1], EncKey[3], data[3]))
        msg.append(Dec(System_para, PP, Sk_ID[1], EncKey[4], data[4]))
        msg.append(Dec(System_para, PP, Sk_ID[2], EncKey[5], data[5]))
        msg.append(Dec(System_para, PP, Sk_ID[2], EncKey[6], data[6]))
        end4 = time.time()
        DecTime = (end4 - start4)*1000

        for i in range(len(msg)):
            print(msg[i])
        # クライアント接続を閉じる
        client.close()

        end_getData = time.time()
        time_getData = (end_getData - start_getData)*1000
        print("データの閲覧に成功しました")

        print("Setup:%f ms" % SetupTime)
        print("SkGen:%f ms" % SkGenTime)
        print("Enc:%f ms" % EncTime)
        print("Dec:%f ms" % DecTime)
        print("Upload:%f ms" % time_upload)
        print("GetData:%f ms" % time_getData)


