import os
from HIBE import *
import pickle

def write(file_path, data):
        # ファイルを開く（存在しない場合は作成される）
    with open(file_path, 'wb') as file:
        # ファイルにテキストを書き込む
        pickle.dump(data, file)

def checkRead(file_path):
    # ファイルを読み込みモードで開く
    with open(file_path, 'rb') as file:
    # ファイルの全内容を読み込む
        content = file.read()
    return content

def checkEncAndWrite(System_para, PP, MK, ID):
    max_level = 5
    EncKey=[]
    Sk_ID=[]
    time3 = []#encの計測用配列

    start2 = time.time()#keyGenの計測
    Sk_ID.append(SkGen(System_para, PP, MK, ID[0]))
    end2 = time.time()
    SkGenTime = (end2 - start2)*1000


    file_path = "fileSize/200mbFile.txt"
    file_path_write = "fileSize_write/200mbFile.txt"
    plaintext = checkRead(file_path)
    start3 = time.time()
    Enc_key, Enc_message = Enc(System_para, PP, ID[0], plaintext)
    end3 = time.time()
    EncTime = (end3 - start3)*1000
    EncKey.append(Enc_key)
    print(file_path,"encTime:",EncTime,"ms")
    write(file_path_write, Enc_message)
    
    print("finish writing")
    print(file_path)
    print(file_path_write)
    return Sk_ID, EncKey, SkGenTime, EncTime

if __name__ == "__main__":
    Sk_ID,EncKey = encAndWrite()
