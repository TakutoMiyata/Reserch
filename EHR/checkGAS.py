from web3 import Web3, HTTPProvider
import ipfshttpclient
from addToIPFS import addToIPFS
import json
from stealthAddr import *
from addData_fileNumber import addData
from getData import getData
import os
from HIBE import *
import pickle
#from writeToFile import encAndWrite
from checkWriteToFile_fileNumber import * 
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

    #for n in range(10):
    #    print("start",n)
    empty_folder("fileNumber_write")
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
        stealthAddr, USK, R, P, names = addData("fileNumber_write")#ファイルをIPFSに乗っける
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

        """
        content = [0]*len(names)
        for i in range(len(content)):
            try:
                # 文字列から数字だけを抽出
                extracted_number = ''.join([char for char in names[i] if char.isdigit()])
                # 抽出した数字の文字列が空の場合はこのイテレーションをスキップ
                if not extracted_number:
                    continue  # 次のイテレーションに進む
                # 数字の文字列が空でない場合は整数に変換して処理を続ける
                number = int(extracted_number)
                print(number)
                content[number] = client.cat(ipfsAddr[number])
            except ipfshttpclient.exceptions.ErrorResponse as e:
                if "this dag node is a directory" in str(e):
                    print(f"The hash {number} is a directory, skipping.")
                else:
                    raise e
        """#うまくいかない

        """
        # ファイル名とIPFSアドレスのマッピング
        file_ipfs_mapping = {
            "fileNumber_write/mbFile_17.txt": "QmPAjaLq8DjE6AKX5Fh4JaiL7CAXYaCuyM55XbjpGLfKN2",
        }
        # ファイル名から数字を抽出し、その数字とIPFSアドレスをタプルとしてリストに格納
        numbers_ipfs = []
        for name, addr in file_ipfs_mapping.items():
            # "fileNumber_write/mbFile_番号.txt" の形式から数字部分を抽出
            # まず "mbFile_番号.txt" 部分を取得
            file_part = name.split('/')[-1]  # パスの最後の部分を取得
            # 次に "mbFile_番号" 部分から数字を抽出
            number = int(file_part.split('_')[1].split('.')[0])
            numbers_ipfs.append((number, addr))

        # 数字でソート
        numbers_ipfs_sorted = sorted(numbers_ipfs, key=lambda x: x[0])

        # contentリストに昇順でデータを追加
        content = []
        for _, addr in numbers_ipfs_sorted:
            content.append(client.cat(addr))

        """#うまくいかない

        content = []
        content.append(client.cat(ipfsAddr[0]))

        data = []
        for i in range(len(content)):   
            data.append(pickle.loads(content[i]))    

        msg = []
        start4 = time.time()
        for i in range(len(content)):
            msg.append(Dec(System_para, PP, Sk_ID[0], EncKey[i], data[i]))#バイナリ形式で帰ってくる
            print(i,"OK")
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

        #time_upload_array[n] = time_upload
        #time_getData_array[n] = time_getData
        
        
        print("Setup:%f ms" % SetupTime)
        print("SkGen:%f ms" % SkGenTime)
        print("Enc:%f ms" % EncTime)
        print("Dec:%f ms" % DecTime)
        
        print("Upload:%f s" % time_upload)
        print("GetData:%f s" % time_getData)

