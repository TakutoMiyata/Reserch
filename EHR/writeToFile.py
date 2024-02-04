import os
from HIBE import *
import pickle

def write(file_path, data):
        # ファイルを開く（存在しない場合は作成される）
    with open(file_path, 'wb') as file:
        # ファイルにテキストを書き込む
        pickle.dump(data, file)

def encAndWrite():
    max_level = 5
    System_para, PP, MK = Setup(max_level)
    EncKey=[]
    ID=[]
    Sk_ID=[]

    ID.append(["0xd691b959f1624B4b721e58a6DcEf363fEDA1D4F1"])#ブロックチェーンのアドレス
    ID.append(["0xd691b959f1624B4b721e58a6DcEf363fEDA1D4F1","0xD3C6d21cdCAA34EcFb5A2ca57C9096506ed88131"])
    ID.append(["0xd691b959f1624B4b721e58a6DcEf363fEDA1D4F1", "0xD3C6d21cdCAA34EcFb5A2ca57C9096506ed88131", "0x67c9268ded4162756429Fef09c7D673Efd906Dd1"])
    
    Sk_ID.append(SkGen(System_para, PP, MK, ID[0]))
    Sk_ID.append(SkDel(System_para, PP, Sk_ID[0], ID[1]))
    Sk_ID.append(SkDel(System_para, PP, Sk_ID[1], ID[2]))

    file_path = "otameshiFolder/otameshi1.txt"
    plaintext = file_path.encode()
    Enc_key, Enc_message = Enc(System_para, PP, ID[0], plaintext)
    EncKey.append(Enc_key)
    data = Dec(System_para, PP, Sk_ID[0], EncKey[0], Enc_message)
    print("original:",plaintext)
    #print("encMsg:",Enc_message)
    print("decrypted:",data)
    write(file_path, Enc_message)

    file_path = "otameshiFolder/otameshi2.txt"
    plaintext = file_path.encode()
    Enc_key, Enc_message = Enc(System_para, PP, ID[0], plaintext)
    EncKey.append(Enc_key)
    data = Dec(System_para, PP, Sk_ID[0], EncKey[1], Enc_message)
    print("original:",plaintext)
    print("decrypted:",data)
    write(file_path, Enc_message)

    file_path = "otameshiFolder/otameshi3.txt"
    plaintext = file_path.encode()
    Enc_key, Enc_message = Enc(System_para, PP, ID[0], plaintext)
    EncKey.append(Enc_key)   
    data = Dec(System_para, PP, Sk_ID[0], EncKey[2], Enc_message)
    print("original:",plaintext)
    print("decrypted:",data)
    write(file_path, Enc_message)

    file_path = "otameshiFolder/otameshiOtameshiFolder/otameshiOtameshi1.txt"
    plaintext = file_path.encode()
    Enc_key, Enc_message = Enc(System_para, PP, ID[1], plaintext)
    EncKey.append(Enc_key)
    data = Dec(System_para, PP, Sk_ID[1], EncKey[3], Enc_message)
    print("original:",plaintext)
    print("decrypted:",data)
    write(file_path, Enc_message)

    file_path = "otameshiFolder/otameshiOtameshiFolder/otameshiOtameshi2.txt"
    plaintext = file_path.encode()
    Enc_key, Enc_message = Enc(System_para, PP, ID[1], plaintext)
    EncKey.append(Enc_key)
    data = Dec(System_para, PP, Sk_ID[1], EncKey[4], Enc_message)
    print("original:",plaintext)
    print("decrypted:",data) 
    write(file_path, Enc_message)

    file_path = "otameshiFolder/otameshiOtameshiFolder/otameshi#Folder/otameshi#1.txt"
    plaintext = file_path.encode()
    Enc_key, Enc_message = Enc(System_para, PP, ID[2], plaintext)
    EncKey.append(Enc_key)
    data = Dec(System_para, PP, Sk_ID[2], EncKey[5], Enc_message)
    print("original:",plaintext)
    print("decrypted:",data)    
    write(file_path, Enc_message)

    file_path = "otameshiFolder/otameshiOtameshiFolder/otameshi#Folder/otameshi#2.txt"
    plaintext = file_path.encode()
    Enc_key, Enc_message = Enc(System_para, PP, ID[2], plaintext)
    EncKey.append(Enc_key)
    data = Dec(System_para, PP, Sk_ID[2], EncKey[6], Enc_message)
    print("original:",plaintext)
    print("decrypted:",data)
    write(file_path, Enc_message)
    
    print("finish writing")
    return System_para, PP, ID, Sk_ID, EncKey

if __name__ == "__main__":
    ID, Sk_ID,EncKey = encAndWrite()
