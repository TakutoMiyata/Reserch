# 用户端：生成hash链、发布任务、解密、发送hash值
import socket

from web3 import Web3
import web3
import json
import time
import sys
import random
import copy
from web3.contract import ConciseContract

from solc import compile_files

from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
from charm.toolbox.secretutil import SecretUtil
from charm.toolbox.ABEnc import ABEnc, Input, Output
from charm.toolbox.ecgroup import ECGroup,G
from charm.toolbox.eccurve import secp384r1
from charm.schemes.pksig.pksig_ecdsa import ECDSA
import hashlib
import pickle
import random

debug = False

class ABEO(ABEnc):

    def __init__(self, groupObj):
        ABEnc.__init__(self)
        global util, group
        util = SecretUtil(groupObj, debug)        
        self.group = groupObj
        

     
    def setup(self):
        g = self.group.random(G1)
        w = self.group.random(G2)
        v = self.group.random(G2)
        u = self.group.random(G2)
        h = self.group.random(G2)
        gp = self.group.random(G2)
        alpha = self.group.random(ZR)
        msk = gp ** alpha
        e_gg_alpha = pair(g,msk)
        pk = {'g':g,'w':w,'v':v,'u':u,'h':h,'e_gg_alpha':e_gg_alpha}
        pksend =  {'g':self.group.serialize(g),'w':self.group.serialize(w),'v':self.group.serialize(v),'u':self.group.serialize(u),'h':self.group.serialize(h),'e_gg_alpha':self.group.serialize(e_gg_alpha)}
        
        return (pk, msk,pksend)
    
    def privKeygen(self, pk, msk, attr_str):
        r = self.group.random(ZR)
        g = pk['g']
        w = pk['w']
        v = pk['v']
        h = pk['h']
        u = pk['u']
        sk1 = msk * (w ** r)
        sk2 = g ** r
        sk_i_3 = {}
        sk_i_4 = {}
        attr = {}
        for a_i in attr_str:
            r_i = self.group.random()
            attr[a_i] = self.group.hash(a_i)
            sk_i_3[a_i] = g ** r_i
            sk_i_4[a_i] = (((u ** attr[a_i]) * h) ** r_i) / (v ** r) 
        sk = {'sk1':sk1,'sk2':sk2,'sk_i_3':sk_i_3,'sk_i_4':sk_i_4,'attr':attr}
        
        return sk


    def tranKeygen(self, sk):
        t0 = self.group.random(ZR)
        tk1 = sk['sk1'] ** t0
        tk2 = sk['sk2'] ** t0
        tk3 = {}
        tk4 = {}
        tk3_send = {}
        tk4_send = {}
        for i in sk['attr']:
            tk3[i] = sk['sk_i_3'][i] ** t0
            tk3_send[i] = self.group.serialize(tk3[i])
        for i in sk['attr']:
            tk4[i] = sk['sk_i_4'][i] ** t0
            tk4_send[i] = self.group.serialize(tk4[i])
        dk = t0 
        tk = {'tk1':tk1,'tk2':tk2,'tk3':tk3,'tk4':tk4}
        tk_send = {'tk1':self.group.serialize(tk1),'tk2':self.group.serialize(tk2),'tk3':tk3_send,'tk4':tk4_send}
       
        return(tk, dk,tk_send)
    
    def veriKeygen(self, tk, pk, attr):
        t1 = self.group.random(ZR)
        rpr = self.group.random(ZR)  
        vk1 = (tk['tk1'] * (pk['w'] ** rpr)) ** t1
        
        vk2 = (tk['tk2'] * (pk['g'] ** rpr)) ** t1
        vk3 = {}
        vk4 = {}
        vk3_send = {}
        vk4_send = {}
        ripr = {}
        for a_i in attr:
            ripr[a_i] = self.group.random(ZR)
            vk3[a_i] = (tk['tk3'][a_i] * (pk['g'] ** ripr[a_i])) ** t1
            vk3_send[a_i] = self.group.serialize(vk3[a_i])

            vk4[a_i] = (tk['tk4'][a_i] * (((pk['u'] ** attr[a_i]) * pk['h']) ** ripr[a_i]) * (pk['v'] ** (-rpr))) ** t1
            vk4_send[a_i] = self.group.serialize(vk4[a_i])

        wk = t1
        vk = {'vk1':vk1,'vk2':vk2,'vk3':vk3,'vk4':vk4}
        rkeys = {'attr':attr,'rpr':rpr,'ripr':ripr}
        vk_send = {'vk1':self.group.serialize(vk1),'vk2':self.group.serialize(vk2),'vk3':vk3_send,'vk4':vk4_send}

        return (vk, rkeys,wk,vk_send)

    def decrypt(self,CT_pr, dk):
        return CT_pr['C0']/(CT_pr['C_0_pr'] ** (1/dk))
    
def getattr(MAX):
    attr_str = []
    for i in range(MAX):
        attr_str.append(str(i+1))
    return attr_str

# 生成哈希链
def generateHashChain(n,hashstr):
    result = []
    result.append(hashlib.sha256(str(hashstr).encode()).digest())
    for i in range(n-1):
        temphash = result[i]
        result.append(hashlib.sha256(temphash).digest())
        temphash = result[i+1]
    return result
        
# 生成merkle根
def generateMerkleRoot(rkeysstr):
    return hashlib.sha256(rkeysstr.encode()).hexdigest()


def main():
    t1 = t2  = 0
    # 签名公钥
    group = ECGroup(secp384r1)
    ecdsa = ECDSA(group)
    public_keystr = {}
    public_key = {}
    public_keystr['g'] = "1:A+w/Vl2rlRovIG3ONL/cQTZC/ZXTP4lE30d1sSCLXk9j0mQGH8hikHxE4NCSCYhPgQ=="
    public_keystr['y'] = "1:A7a9qTqQVIRm+aa1m/LPPKYvvMqp5QR+GBStCfUlA6clbf0n8jKEjl3k3Fmh7knqOw=="
    public_key['g'] = group.deserialize(public_keystr['g'].encode())
    public_key['y'] = group.deserialize(public_keystr['y'].encode())

    # 生成用户属性以及访问策略
    n = 100 
    price = 1
    attr_str = getattr(25)
    # 群参数初始化

    groupObj = PairingGroup('SS512')
    abeo = ABEO(groupObj)

    

    (pk,msk,pksend) = abeo.setup()
    sk = abeo.privKeygen(pk, msk, attr_str)
    (tk,dk,tksend) = abeo.tranKeygen(sk)
    (vk,rkeys,wk,vksend) = abeo.veriKeygen(tk,pk,sk['attr'])
   
    #生成hashchain
    hashstr = "this is a hashchain"
    hashchain = generateHashChain(n+1,hasattr)

    keysstr = str(pk) + str(tk) + str(vk) 
    # 生成转化秘钥和验证秘钥的merkle根
    keyshash =hashlib.sha256(keysstr.encode()).hexdigest()
    #生成hashchain
    hashstr = "this is a hashchain"
    hashchain = generateHashChain(n+1,hasattr)

# ----------------部署合约--------------
    
    w3 = Web3(Web3.HTTPProvider("http://101.76.219.50:8545"))
    user = w3.eth.accounts[0]
    w3.personal.unlockAccount(user,'')    
    compile_sol = compile_files(['/home/pi/ABEO.sol'])
    contractid, contract_interface = compile_sol.popitem()
    start = time.time()
    tx_hash = w3.eth.contract(abi=contract_interface['abi'],bytecode=contract_interface['bin']).constructor(hashchain[n],n,keyshash).transact({'from':user,'value':int(n*price),'gas':4000000})
    
    # print(w3.eth.getTransactionReceipt(tx_hash))
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash,timeout=360)
    t1 = time.time() - start
    # print("用户账户余额：",w3.eth.getBalance(user))

    contract_address = tx_receipt['contractAddress']

#---------------------- 建立tcp链接-----------------------
    
    host = '39.100.39.114'
    port = 5005
    BUFFER_SIZE = 4096
   
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    # print("maxsize:",s.getsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF))
# -----------------公布合约地址，以及ABI----------------
    s.sendall(contract_address.encode('utf-8'))
    data = s.recv(BUFFER_SIZE)

    s.sendall(pickle.dumps(contract_interface['abi']))
    data = s.recv(BUFFER_SIZE)


# -----------------公钥,转化秘钥发送-----------------

    s.sendall(pickle.dumps(pksend))
    data = s.recv(BUFFER_SIZE)
    # print(data)
    tksend_temp = pickle.dumps(tksend)
    length = len(tksend_temp)
    # print("tk length:",len(pickle.dumps(tksend)))
    
    s.sendall(str(length).encode('utf-8'))
    data = s.recv(BUFFER_SIZE)

    # print("tk:",tk)
    # print("tk size:",len(pickle.dumps(tksend)))
    s.sendall(tksend_temp)
    data = s.recv(BUFFER_SIZE)
    # print(data)
    

    s.sendall(pickle.dumps(vksend))
    data = s.recv(BUFFER_SIZE)
    # print(data)

    # 发送属性字符串
    # print(attr_str)
    s.send(pickle.dumps(attr_str))
    

    contract_instance = w3.eth.contract(address=contract_address,abi=contract_interface['abi'])
    

# --------------------用户开始与云交互，交换结果----------------
    last = n
    wronghash = hashlib.sha256("wrong".encode()).digest()
    # wrongnum = random.randint(0,n)
    # 计算全部正确
    wrongnum = n-1
    # 接收转化结果
    for i in range(n):
        data = s.recv(BUFFER_SIZE)
        #print("transform:",i,data)
        transform = pickle.loads(data)
        CT_pr = {}
        CT_pr['C0'] = groupObj.deserialize(transform['CT_pr']['C0'])
        CT_pr['C_0_pr'] = groupObj.deserialize(transform['CT_pr']['C_0_pr'])
        sig = {}
        sig['r'] = group.deserialize(transform['sig']['r'])
        sig['s'] = group.deserialize(transform['sig']['s'])
        ok = ecdsa.verify(public_key,sig,str(CT_pr))
        m_pr = abeo.decrypt(CT_pr,dk)
        # 解密出错，发送出错信号
        if i == wrongnum:
            # print(i,"is wrong")
            last = i
            s.send(wronghash)
            break
        # 发送hash值
        hashvalue = hashchain[n-1-i]
        s.send(hashvalue)

    # print("部署合约：",t1)
# ----------------开始申请矿工仲裁提供pk,tk,vk,以及各种参数
    if last is not n:
        start = time.time()
        tx_hash = contract_instance.functions.verifyTkVk(str(pk) + "#",str(tk) + "#",str(vk) + "#",str(rkeys) + "#",str(wk)+"#").transact({'from':user,'gas':40000000})
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        t = time.time() - start
        print("TV:",t)
    # print("time:",time.time() - start)
    time.sleep(5)    
    
    print("用户账户余额：",w3.eth.getBalance(user))
    s.close()
    return

    

if __name__ == "__main__":
    main()
