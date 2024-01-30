import time
from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair
import numpy as np
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import hashlib


group = PairingGroup("MNT159")  #こっちのが速いがセキュリティはビミョー
#group = PairingGroup("SS512")  #こっちのがセキュリティはいいが遅い

def setup(max_level):
    g = group.random(G1)
    alpha = group.random(ZR)
    g1 = g ** alpha

    c1 = group.random(G2)
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

    h_PK_ID_c2 = [x * c2 for x in h_PK_ID]  # h_PK_ID の各要素に c2 を乗算
    h_PK_ID_c2_r = [x ** r for x in h_PK_ID_c2]  # 結果のリストに r のべき乗を適用
    msk_PK = [msk * x for x in h_PK_ID_c2_r]

    SK_ID = (msk_PK, g ** r, h_r_now)

    return PK_ID, SK_ID

def derive(SK_ID, msk): #今ここ
    r_ = group.random(ZR)
    t = group.random(ZR)

def encrypt(msg, ID, s, level, PK_ID, params):
    h = params[4]
    h_PK_ID = [h[i] ** PK_ID[i] for i in range(level)]

    # 鍵生成: G1群のランダムな要素
    key_element = group.random(G1)
    # AESキーとして使用するために、鍵をバイト列に変換
    raw_key = group.serialize(key_element)
    # AESキーの長さを適切に調整（例：AES-256の場合は32バイト）
    #aes_key = raw_key[:32]
    # AES-256用に32バイトにハッシュ化
    aes_key = hashlib.sha256(raw_key).digest()

    # 初期化ベクトル（IV）の生成（AESブロックサイズに合わせる）
    iv = os.urandom(16)

    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    msg_bytes = msg.encode()
    ct = encryptor.update(msg_bytes) + encryptor.finalize()

    g = params[0]
    g1 = params[1]
    c1 = params[2]
    c2 = params[3]
    e = pair(g1,c1)

    CT = ((e**s)*aes_key, g**s, (h_PK_ID*c2)**s, ct)

    return CT, aes_key, iv


def decrypt(PK_ID, SK_ID, CT, iv):
    (A,B,C,D) = CT
    # b[max_level - level]
    (a0, a1, b) = SK_ID

    aes_key = A*pair(a1,C)/pair(B,a0)
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    msg_bytes = decryptor.update(D) + decryptor.finalize()
    msg = msg_bytes.decode()

    return msg

if __name__ == "__main__":
    max_level = 3

    params, msk= setup(max_level)

    level = 3 #ID's level
    ID = "miyata"
    msg = "Hello World."

    s = group.random(ZR)
    r = group.random(ZR)
    PK_ID, SK_ID = Keygen(msk, level, ID, s, r, params)


    CT ,aes_key, iv = encrypt(msg, ID, s, level, PK_ID, params)
    msg_ = decrypt(PK_ID, SK_ID, CT, iv)

    if msg == msg_:
        print("CORRECT!")
    else:
        print("MISTAKE...")