from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair
import numpy as np

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

if __name__ == "__main__":
    P = 10 #seed　多分なんでもいい
    ID_string = "0xe22694a13837DA6bC13B666b37A5Cb321B654b49"
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
