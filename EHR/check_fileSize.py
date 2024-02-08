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
#from writeToFile import encAndWrite
from checkWriteToFile_fileSize import * 
from operateDoctor import *
import time
from emptyFolder import *
import numpy as np
import matplotlib.pyplot as plt
import csv

if __name__ == "__main__":
    #seed = 0 #患者が自分のデータを登録，確認する場合．
    seed = 1 #患者がデータを登録し，病院側がデータを閲覧する場合．
    time_upload_array = np.zeros(10)
    time_getData_array = np.zeros(10)

    for n in range(10):
        print("start",n)
        empty_folder("fileSize_write")
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
            """
            ID.append(["0xd691b959f1624B4b721e58a6DcEf363fEDA1D4F1","0xD3C6d21cdCAA34EcFb5A2ca57C9096506ed88131"])
            ID.append(["0xd691b959f1624B4b721e58a6DcEf363fEDA1D4F1", "0x67c9268ded4162756429Fef09c7D673Efd906Dd1"])
            ID.append(["0xd691b959f1624B4b721e58a6DcEf363fEDA1D4F1", "0x08aCA4CbC3298545A20e397FdDD77b0AA2704aC8"])
            ID.append(["0xd691b959f1624B4b721e58a6DcEf363fEDA1D4F1", "0x77531B71944Cae1714955863314708B5F56e3491"])
            ID.append(["0xd691b959f1624B4b721e58a6DcEf363fEDA1D4F1", "0xD3C6d21cdCAA34EcFb5A2ca57C9096506ed88131", "0x93EED64b7bF4B7b685c1EB74c70744cb38ae3535"])
            ID.append(["0xd691b959f1624B4b721e58a6DcEf363fEDA1D4F1", "0xD3C6d21cdCAA34EcFb5A2ca57C9096506ed88131", "0x5A206f543e9a4139CE20EC6a538F5c16Fe3EAC0B"])
            ID.append(["0xd691b959f1624B4b721e58a6DcEf363fEDA1D4F1", "0xD3C6d21cdCAA34EcFb5A2ca57C9096506ed88131", "0xBB8Cb0169E5D488e154d661d3c6142314f888589"])
            ID.append(["0xd691b959f1624B4b721e58a6DcEf363fEDA1D4F1", "0xD3C6d21cdCAA34EcFb5A2ca57C9096506ed88131", "0x72147E0609E612bCd326aEFee7F2a29E79baCf4C"])
            ID.append(["0xd691b959f1624B4b721e58a6DcEf363fEDA1D4F1", "0xD3C6d21cdCAA34EcFb5A2ca57C9096506ed88131", ""])
            ID.append(["0xd691b959f1624B4b721e58a6DcEf363fEDA1D4F1", "0xD3C6d21cdCAA34EcFb5A2ca57C9096506ed88131", "0x47b80aBdc480AEC202c4740b5647a745F684C815"])
            """
            start_upload = time.time()
            
            Sk_ID, EncKey, SkGenTime, EncTime = checkEncAndWrite(System_para, PP, MK, ID)#ファイルに書き込み
            stealthAddr, USK, R, P = addData("fileSize_write")#ファイルをIPFSに乗っける
            print("データの登録を完了しました")

            end_upload = time.time()
            time_upload = (end_upload - start_upload)
        #データの登録完了
        #------------------------------------------------------------------------------------
            loadFile = json.load(open('./contractAddress.json'))
            Datacontract_address = loadFile["contractData"]# コントラクトのアドレス

            Enc_key, enPermMap = makeEnPermMap(Datacontract_address, ID, System_para, PP)
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
            content.append(client.cat(ipfsAddr[0]))

            data = []
            for i in range(len(content)):   
                data.append(pickle.loads(content[i]))

            msg = []
            start4 = time.time()
            msg.append(Dec(System_para, PP, Sk_ID[0], EncKey[0], data[0]))#バイナリ形式で帰ってくる
            """
            msg.append(Dec(System_para, PP, Sk_ID[0], EncKey[1], data[1]))
            msg.append(Dec(System_para, PP, Sk_ID[0], EncKey[2], data[2]))
            msg.append(Dec(System_para, PP, Sk_ID[1], EncKey[3], data[3]))
            msg.append(Dec(System_para, PP, Sk_ID[1], EncKey[4], data[4]))
            msg.append(Dec(System_para, PP, Sk_ID[2], EncKey[5], data[5]))
            msg.append(Dec(System_para, PP, Sk_ID[2], EncKey[6], data[6]))
            """
            end4 = time.time()
            DecTime = (end4 - start4)*1000

            """
            for i in range(len(msg)):
                print(msg[i])
            """
            # クライアント接続を閉じる
            client.close()

            end_getData = time.time()
            time_getData = (end_getData - start_getData)
            print("データの閲覧に成功しました")

            time_upload_array[n] = time_upload
            time_getData_array[n] = time_getData
            
            """
            print("Setup:%f ms" % SetupTime)
            print("SkGen:%f ms" % SkGenTime)
            print("Enc:%f ms" % EncTime)
            print("Dec:%f ms" % DecTime)
            """
            print("Upload:%f s" % time_upload)
            print("GetData:%f s" % time_getData)

    # csvに保存
    averageUpload = (np.mean(time_upload_array))*1000
    averageGetData = (np.mean(time_getData_array))*1000
    fileSize = (10**8)*2
    data = list(zip([averageUpload], [averageGetData], [fileSize]))
    
    with open("ExecutionTimeData/fileSizeChanze.csv", "a", newline="") as csvfile:
        try:
            csvwriter = csv.writer(csvfile)
            #csvwriter.writerow(["averageUpload", "averageGetData", "fileSize"])
            csvwriter.writerows(data)
            print("Finish writing csvfile")
        except Exception as e:
            print(f"Error wrting csvfile: {e}")
    