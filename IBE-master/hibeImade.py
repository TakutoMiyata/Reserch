import time
from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair, extract_key
import numpy as np
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import hashlib
from functools import reduce
from charm.toolbox.symcrypto import AuthenticatedCryptoAbstraction
from charm.core.math.pairing import pairing
import operator


group = PairingGroup("MNT159")  #こっちのが速いがセキュリティはビミョー
#group = PairingGroup("SS512")  #こっちのがセキュリティはいいが遅い

def setup(max_level):
    g = group.random(G2)
    alpha = group.random(ZR)
    g1 = g ** alpha

    c1 = group.random(G1)
    c2 = group.random(G1) 

    h = [group.random(G1) for i in range(max_level)]
    params = (g, g1, c1, c2, h)

    msk = c1 ** alpha

    return params, msk

def Keygen(msk, level, ID, s, r, params):
    PK_ID = [group.hash(i) for i in ID] #IDをZRの要素に変換
    g = params[0]
    c2 = params[3]
    h = params[4]

    h_PK_ID = [h[i] ** PK_ID[i] for i in range(level)]
    h_r_now = [h[j+1]**r for j in range(max_level - level)]

    h_PK_ID_c2 = reduce(operator.mul, h_PK_ID, 1) * c2
    h_PK_ID_c2_r = h_PK_ID_c2 ** r
    msk_h = msk * h_PK_ID_c2_r
    SK_ID = (msk_h, g ** r, h_r_now)

    return PK_ID, SK_ID

def delive(SK_ID, msk):
    r_ = group.random(ZR)
    t = group.random(ZR)

def encrypt(msg, s, level, PK_ID, params):
    g = params[0]
    g1 = params[1]
    c1 = params[2]
    c2 = params[3]
    h = params[4]

    h_PK_ID = [h[i] ** PK_ID[i] for i in range(level)]
    h_PK_ID_c2 = reduce(operator.mul, h_PK_ID, 1) * c2
    h_PK_ID_c2_s = h_PK_ID_c2 ** s

    # 鍵生成: G1群のランダムな要素
    key_element = group.random(GT)
    # AESキーとして使用するために、鍵をバイト列に変換
    symmetric_key = extract_key(key_element)
    enc_cipher = AuthenticatedCryptoAbstraction(symmetric_key)
    ct = enc_cipher.encrypt(msg)

    e = pair(g1,c1)
    # e**s の結果をバイト列に変換
    es = e ** s

    combined_key = es * key_element

    # CT の計算
    CT = (combined_key, g**s, h_PK_ID_c2_s, ct)

    return CT, symmetric_key


def decrypt(PK_ID, SK_ID, CT):
    (A,B,C,D) = CT
    # b[max_level - level]
    (a0, a1, b) = SK_ID
    # C と a1 のペアリングを計算
    paired_C_a1 = pair(a1, C)
    # B と a0 のペアリングを計算
    paired_B_a0 = pair(B, a0)

    symmetric_key_element = A*(paired_C_a1 / paired_B_a0)
    symmetric_key = extract_key(symmetric_key_element)
    dec_cipher = AuthenticatedCryptoAbstraction(symmetric_key)
    msg = dec_cipher.decrypt(D)
    
    #X = symmetric_key_element
    X = symmetric_key
    return msg, X

if __name__ == "__main__":
    max_level = 3

    params, msk= setup(max_level)

    level = 3 #ID's level
    ID = "miyata"
    msg = "Hello World."

    s = group.random(ZR)
    r = group.random(ZR)
    PK_ID, SK_ID = Keygen(msk, level, ID, s, r, params)


    CT ,symmetric_key = encrypt(msg, s, level, PK_ID, params)
    msg_, X = decrypt(PK_ID, SK_ID, CT)
    msg_ = msg_.decode('utf-8')


    if msg == msg_:
        print("CORRECT!")
    else:
        print("MISS...")
        print(msg)
        print(msg_)
        if symmetric_key == X:
            print("key OK")
        else:
            print("key miss")