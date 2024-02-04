from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair
import numpy as np
import binascii


group = PairingGroup("MNT159")

def setup(P):
    msk = group.random(ZR,1,P)
    MPK = msk*P

    return msk, MPK

def keyGen(ID,MPK,P):
    msk = MPK/P
    UPK = group.hash(ID,G1)
    USK = msk * UPK

    return UPK, USK

def addrGen(ID,MPK,P):
    UPK = group.hash(ID,G1)
    r = group.random(ZR)
    pair_result = pair(r*MPK,UPK)
    binary_pair_result = group.serialize(pair_result)
    hashed_result = group.hash(binary_pair_result, ZR)

    ADDR = hashed_result * P
    R = r*P

    return ADDR, R

def recoverAddr(ADDR,R,USK,P):
    pair_result = pair(R,USK)
    binary_pair_result = group.serialize(pair_result)
    hashed_result = group.hash(binary_pair_result, ZR)

    tsk = hashed_result
    ADDR_ = tsk*P

    return ADDR_

def generate_address_for_id(ID_string, P):
    ID = ID_string.encode('utf-8')
    msk, MPK = setup(P)
    ADDR, R = addrGen(ID, MPK, P)
    return ADDR

def convert_addr_to_string(ADDR):#文字列に変換
    # ADDRをバイナリ（バイト列）にシリアライズする
    binary_data = group.serialize(ADDR)
    
    # バイナリデータを16進数の文字列に変換する
    hex_string = binascii.hexlify(binary_data).decode('utf-8')
    
    return hex_string

def convert_string_to_addr(hex_string):#stealthAddrの元の形に戻す
    # 16進数の文字列をバイナリデータに変換
    binary_data = binascii.unhexlify(hex_string)
    
    # バイナリデータを元のADDRオブジェクトにデシリアライズ
    ADDR = group.deserialize(binary_data)
    
    return ADDR


if __name__ == "__main__":
    P = 10 #seed　多分なんでもいい
    ID_string = "0xd691b959f1624B4b721e58a6DcEf363fEDA1D4F1"
    ID = ID_string.encode('utf-8')
    msk, MPK = setup(P)
    UPK, USK = keyGen(ID,MPK,P)
    ADDR, R = addrGen(ID,MPK,P)
    ADDR_ = recoverAddr(ADDR,R,USK,P)

    if ADDR == ADDR_:
        print(ID_string)
        print(ID)
        print(ADDR)
        print(ADDR_)
        print("correct")
    else:
        print("miss")
