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

    for n in range(10):
        print("start",n)
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
                "fileNumber_write/mbFile_26.txt": "QmVBrWbBwo7Fs6WpGVMkA7kRLdwrzP65Ut3iefiQufvPxL",
                "fileNumber_write/mbFile_27.txt": "QmRKq4pAXif522bWpBBXKMjgxJ6bVnuQVjxVHcKF38dPtG",
                "fileNumber_write/mbFile_28.txt": "QmbQBuqszGv9W9XdN6ien4g998zmzjec2rZyDjySbhfYmB",
                "fileNumber_write/mbFile_15.txt": "QmUW8vSkRoQ2x8TxFTiFjDCj6hBRJoJzV2MxGjVMRn5M9g",
                "fileNumber_write/mbFile_20.txt": "QmaT3brUH2xDyqyLGU6MWy22F1qQpBf6FYEMRxMCXh7kJV",
                "fileNumber_write/mbFile_21.txt": "QmQXQAeVJHKEkqcXhdZqsCrx8BzcpwtdowHWa8bzbYz7j5",
                "fileNumber_write/mbFile_22.txt": "Qmas7XKxcgV1n2v2xJhUeYQUQ7T3WtboaEp7L6dqpGvvVR",
                "fileNumber_write/mbFile_0.txt": "QmNeKPqrrv2w1HbBkJySScMQQ3VsTy2Q3ZKySkzwtZXvhE",
                "fileNumber_write/mbFile_1.txt": "Qme9cQmqsL1tyHGpHnFF5FwhF1Czn1fV4MGShUUFA9q4wD",
                "fileNumber_write/mbFile_6.txt": "QmNaGqSieRS4HFABv4C2oDEyjhKViaLnvJsYRsW43XUT5c",
                "fileNumber_write/mbFile_13.txt": "QmZTEoypyqRq3tkwaYmB3H2tTgUXJLvpCFas7wXSirUxSA",
                "fileNumber_write/mbFile_18.txt": "QmTfe5zLZhdE3vTkewHUC7N4DvWVBLKukSNghid2ovfSYg",
                "fileNumber_write/mbFile_12.txt": "QmQCzioWC8mcAQxQNdFtDmksCCrjsHfQPnBaygdFFjdfUE",
                "fileNumber_write/mbFile_23.txt": "QmQrcVNujeAieSYQEjzo2cDDxW2jzm8UU3PnwYmQYR4xQD",
                "fileNumber_write/mbFile_24.txt": "QmWaJZhEthmrAnaRX3Vh5Y7rdkb8kwCKvQ1kgJKfnPSB6E",
                "fileNumber_write/mbFile_16.txt": "QmeVvmscbVrHNyqZYsE5EJUsC58DhT9T5rphsiN6oKy9kc",
                "fileNumber_write/mbFile_29.txt": "QmVNLVotZj8X2cSAZvdDFskFWbH4xU6tVQjt4YuiBxNgnu",
                "fileNumber_write/mbFile_4.txt": "QmVeeat4R1s2r9iE4R91azfhzDCNGX1XF6MNfd7wXAaAh1",
                "fileNumber_write/mbFile_14.txt": "QmXd59czEhTRB2hNGVRQNdLFd5KHVBKNZWSDhsAB91kfRT",
                "fileNumber_write/mbFile_25.txt": "QmTGFmeWco3aTPortXf6YsCetCTvKq6Lp9XTDPuJVdUmzN",
                "fileNumber_write/mbFile_2.txt": "QmbjEztvpQH6cEeyBiV3ZUDk6qEgcB1mKbbp4NvAFfB1ca",
                "fileNumber_write/mbFile_8.txt": "QmYpbtsjs7MMN3VAkFLFsqUbpnGL5TvS3DZzVYDcHCiKch",
                "fileNumber_write/mbFile_11.txt": "QmYVroDeCuohkLAZjYqCSwusR6vvu9WiLzAre2RuhUc4H2",
                "fileNumber_write/mbFile_10.txt": "QmdSUocFxisedHCeYZiWdJnjspEYgD5TRRBzXndk2JuFBj",
                "fileNumber_write/mbFile_3.txt": "Qmf7Cp52gCKZo3gQXqeKZgEc2qyunjEuDb5TD4Vi8nWyS1",
                "fileNumber_write/mbFile_19.txt": "QmSiuoYW4rLFC5pXCNjnCEE2QwDybbG84C1EZx9VQPwqrj",
                "fileNumber_write/mbFile_5.txt": "QmWtLAon7YdHoi8eFHPDMWYJCSymVdAGq2dLKpJvqA5QQo",
                "fileNumber_write/mbFile_9.txt": "QmdEJdyR34hdG2D4vq955hZv2DdCGC1adARwm7z4GbGnpa",
                "fileNumber_write/mbFile_7.txt": "QmV2tZdZBKKCnFtW3BvpdJnumdo2wkh83Rj4Qaj5JpB5Us",
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

            """

            content = []
            content.append(client.cat(ipfsAddr[27]))
            content.append(client.cat(ipfsAddr[28]))
            content.append(client.cat(ipfsAddr[64]))
            content.append(client.cat(ipfsAddr[69]))
            content.append(client.cat(ipfsAddr[53]))
            content.append(client.cat(ipfsAddr[74]))
            content.append(client.cat(ipfsAddr[29]))
            content.append(client.cat(ipfsAddr[79]))
            content.append(client.cat(ipfsAddr[66]))
            content.append(client.cat(ipfsAddr[77]))
            content.append(client.cat(ipfsAddr[68]))
            content.append(client.cat(ipfsAddr[67]))
            content.append(client.cat(ipfsAddr[38]))
            content.append(client.cat(ipfsAddr[30]))
            content.append(client.cat(ipfsAddr[56]))
            content.append(client.cat(ipfsAddr[18]))
            content.append(client.cat(ipfsAddr[50]))
            content.append(client.cat(ipfsAddr[0]))
            content.append(client.cat(ipfsAddr[34]))
            content.append(client.cat(ipfsAddr[70]))
            content.append(client.cat(ipfsAddr[21]))
            content.append(client.cat(ipfsAddr[24]))
            content.append(client.cat(ipfsAddr[25]))          
            content.append(client.cat(ipfsAddr[40]))
            content.append(client.cat(ipfsAddr[47]))
            content.append(client.cat(ipfsAddr[59]))
            content.append(client.cat(ipfsAddr[2]))
            content.append(client.cat(ipfsAddr[9]))
            content.append(client.cat(ipfsAddr[15]))
            content.append(client.cat(ipfsAddr[52]))
            content.append(client.cat(ipfsAddr[36]))
            content.append(client.cat(ipfsAddr[6]))
            content.append(client.cat(ipfsAddr[55]))
            content.append(client.cat(ipfsAddr[10]))
            content.append(client.cat(ipfsAddr[5]))
            content.append(client.cat(ipfsAddr[57]))
            content.append(client.cat(ipfsAddr[49]))
            content.append(client.cat(ipfsAddr[41]))
            content.append(client.cat(ipfsAddr[23]))
            content.append(client.cat(ipfsAddr[26]))
            content.append(client.cat(ipfsAddr[61]))
            content.append(client.cat(ipfsAddr[22]))
            content.append(client.cat(ipfsAddr[46]))
            content.append(client.cat(ipfsAddr[3]))
            content.append(client.cat(ipfsAddr[51]))
            content.append(client.cat(ipfsAddr[12]))
            content.append(client.cat(ipfsAddr[8]))
            content.append(client.cat(ipfsAddr[48]))
            content.append(client.cat(ipfsAddr[19]))
            content.append(client.cat(ipfsAddr[78]))
            content.append(client.cat(ipfsAddr[1]))
            content.append(client.cat(ipfsAddr[16]))
            content.append(client.cat(ipfsAddr[60]))
            content.append(client.cat(ipfsAddr[76]))
            content.append(client.cat(ipfsAddr[42]))
            content.append(client.cat(ipfsAddr[33]))
            content.append(client.cat(ipfsAddr[65]))
            content.append(client.cat(ipfsAddr[20]))
            content.append(client.cat(ipfsAddr[37]))
            content.append(client.cat(ipfsAddr[73]))
            content.append(client.cat(ipfsAddr[17]))
            content.append(client.cat(ipfsAddr[35]))
            content.append(client.cat(ipfsAddr[32]))
            content.append(client.cat(ipfsAddr[4]))
            content.append(client.cat(ipfsAddr[72]))
            content.append(client.cat(ipfsAddr[13]))
            content.append(client.cat(ipfsAddr[7]))
            content.append(client.cat(ipfsAddr[75]))
            content.append(client.cat(ipfsAddr[71]))
            content.append(client.cat(ipfsAddr[44]))
            content.append(client.cat(ipfsAddr[54]))
            content.append(client.cat(ipfsAddr[11]))
            content.append(client.cat(ipfsAddr[31]))
            content.append(client.cat(ipfsAddr[14]))
            content.append(client.cat(ipfsAddr[58]))
            content.append(client.cat(ipfsAddr[62]))
            content.append(client.cat(ipfsAddr[45]))
            content.append(client.cat(ipfsAddr[63]))
            content.append(client.cat(ipfsAddr[43]))
            content.append(client.cat(ipfsAddr[39]))


            




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
    fileNumber = 80
    data = list(zip([averageUpload], [averageGetData], [fileNumber]))
    
    with open("ExecutionTimeData/fileNumberChanze.csv", "a", newline="") as csvfile:
        try:
            csvwriter = csv.writer(csvfile)
            #csvwriter.writerow(["averageUpload", "averageGetData", "fileNumber"])
            csvwriter.writerows(data)
            print("Finish writing csvfile")
        except Exception as e:
            print(f"Error wrting csvfile: {e}")
    