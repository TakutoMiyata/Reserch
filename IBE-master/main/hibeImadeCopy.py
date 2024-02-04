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

def Keygen(msk, level, ID, params, pp):
    PK_ID = [group.hash(i) for i in ID] #IDをZRの要素に変換
    g = params[0]
    c2 = params[3]
    h = params[4]
    if level == 1:
        print("Your level is 1")
        r = group.random(ZR)
    else:
        print("Your level is ",level)
        r = pp
    #r = group.random(ZR) 
    h_PK_ID = [h[i] ** PK_ID[i] for i in range(level)]
    h_r_now = [h[j+1]**r for j in range(max_level+1 - level)]
    print(len(h_r_now))
    h_PK_ID_c2 = reduce(operator.mul, h_PK_ID, 1) * c2
    h_PK_ID_c2_r = h_PK_ID_c2 ** r
    msk_h = msk * h_PK_ID_c2_r
    SK_ID = (msk_h, g ** r, h_r_now)

    return PK_ID, SK_ID

def delive(SK_ID_, msk, params, del_ID):
    level = len(SK_ID)
    max_level = len(params[4])
    len_del_ID = len(del_ID)

    g = params[0]
    gt = g**t
    r_ = group.random(ZR)
    t = group.random(ZR)
    h = params[4]

    # SKTopic|q−1 =(cα ·(hT1 ···hTq−1 ·c2)r ,дr′,hqr′,...,hr′)=(a0,a1,bq,...,bl).
    (a0, a1, b) = (SK_ID_[0], SK_ID_[1], SK_ID_[2])
    # r = r_ + t

    PK_del_ID = [group.hash(i) for i in del_ID] #IDをZRの要素に変換
    h_PK_del_ID = [h[i] ** PK_del_ID[i] for i in range(level)]
    h_PK_del_ID_c2 = reduce(operator.mul, h_PK_del_ID, 1) * c2
    h_PK_ID_c2_t = h_PK_ID_c2 ** t
    
    if level+1 > max_level:
        bh = 0
    else:
        bh = [x * h for x in b[level+1:max_level-1]]

    PK_ID = PK_del_ID
    SK_ID = (a0*b[0]*h_PK_ID_c2_t, a1*gt, bh)
    pp = r

    return PK_ID, SK_ID, pp

def encrypt(msg, level, PK_ID, params):
    g = params[0]
    g1 = params[1]
    c1 = params[2]
    c2 = params[3]
    h = params[4]
    s = group.random(ZR)

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


def decrypt(SK_ID, CT):
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
    X = symmetric_key # デバッグ用
    return msg, X

if __name__ == "__main__":
    max_level = 5
    pp = 0 #継承の初期化
    start1 = time.time()
    params, msk= setup(max_level)
    end1 = time.time()

    level = 3 #ID's level
    ID = "miyata"
    msg = "Hello World."

    start2 = time.time()
    PK_ID, SK_ID = Keygen(msk, level, ID, params, pp)
    end2 = time.time()

    start4 = time.time()
    CT ,symmetric_key = encrypt(msg, level, PK_ID, params)
    end4 = time.time()

    start5 = time.time()
    msg_, X = decrypt(SK_ID, CT)
    msg_ = msg_.decode('utf-8')
    end5 = time.time()

    if msg == msg_:
        print("CORRECT!")
    else:
        print("MISS...")
        print(msg)
        print(msg_)
        if symmetric_key == X:  # デバッグ用
            print("key OK")
        else:
            print("key miss")

    print("Setup:%f ms" % ((end1 - start1)*1000))
    print("SkGen:%f ms" % ((end2 - start2)*1000))
    #print("SkDel:%f s" % ((end3 - start3)*1000))
    print("Enc:%f ms" % ((end4 - start4)*1000))
    print("Dec:%f ms" % ((end5 - start5)*1000))

