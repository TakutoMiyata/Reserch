# 云：转化计算、支付、验证
'''
!!每个密文对应不同的策略还是相同的策略，根据论文的描述，每个密文使用不同的策略
是否存在, 用户的属性不满足policy的情况？
设定一定的成功比例？数据的有效率？用户只会获得有权限访问的数据
'''
from web3 import Web3
import web3
from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
from charm.toolbox.secretutil import SecretUtil
from charm.toolbox.ABEnc import ABEnc, Input, Output
from charm.toolbox.ecgroup import ECGroup,G
from charm.toolbox.eccurve import secp384r1
from charm.schemes.pksig.pksig_ecdsa import ECDSA
import hashlib

import time
import random
import hashlib 

import socket
import pickle
from socket import SHUT_RDWR

from pprint import pprint
class ABEO(ABEnc):

    def __init__(self, groupObj):
        ABEnc.__init__(self)
        global util, group
        util = SecretUtil(groupObj, False)        
        self.group = groupObj
    
# ------cloud----------------------------------
    def getPk(self,pk):
        for (x,y) in pk.items():
            pk[x] = self.group.deserialize(y)
        return pk

    def getTk(self,tk):
        tk['tk1'] = self.group.deserialize(tk['tk1'])
        tk['tk2'] = self.group.deserialize(tk['tk2'])
        for (x,y) in tk['tk3'].items():
            tk['tk3'][x] = self.group.deserialize(y)
        for (x,y) in tk['tk4'].items():
            tk['tk4'][x] = self.group.deserialize(y)
        return tk
    
    
    def getVk(self,vk):
        vk['vk1'] = self.group.deserialize(vk['vk1'])
        vk['vk2'] = self.group.deserialize(vk['vk2'])
        for (x,y) in vk['vk3'].items():
            vk['vk3'][x] = self.group.deserialize(y)
        for (x,y) in vk['vk4'].items():
            vk['vk4'][x] = self.group.deserialize(y)
        return vk


    def tranform(self, tk, CT,attr_str):
        policy = util.createPolicy(CT['policy_str'])
        pruned = util.prune(policy,attr_str)
        # 不满足策略
        if pruned == False:
            return False
        coeffs = util.getCoefficients(policy)
        w_i = {}
        C_i_2 = CT['C_i_2']
        C_i_3 = CT['C_i_3']
        C_i_4 = CT['C_i_4']
        temp1 = 1
        
        for i in pruned:
            j = i.getAttributeAndIndex()
            k = i.getAttribute()
            w_i[j] = coeffs[j]
            temp1 *= (pair(C_i_2[j] **w_i[j],tk['tk2']) * pair(C_i_3[j] **w_i[j],tk['tk3'][k]) * pair(C_i_4[j]** w_i[j], tk['tk4'][k]))
            
        
        C_0_pr = pair(CT['C1'],tk['tk1']) / temp1
    
        CT_pr = {'C0':CT['C0'],'C_0_pr':C_0_pr}

        return CT_pr
    def tranform2(self, vk, CT,attr_str):
        policy = util.createPolicy(CT['policy_str'])
        pruned = util.prune(policy,attr_str)
        # 不满足策略
        if pruned == False:
            return False
        coeffs = util.getCoefficients(policy)
        w_i = {}
        C_i_2 = CT['C_i_2']
        C_i_3 = CT['C_i_3']
        C_i_4 = CT['C_i_4']
        
        temp2 = 1
        for i in pruned:
            j = i.getAttributeAndIndex()
            k = i.getAttribute()
            w_i[j] = coeffs[j]
            temp2 *= (pair(C_i_2[j] **w_i[j],vk['vk2']) * pair(C_i_3[j] **w_i[j],vk['vk3'][k]) * pair(vk['vk4'][k], C_i_4[j]** w_i[j]))
        
        C_1_pr = pair(CT['C1'],vk['vk1'])/temp2

        return C_1_pr
# -------------dataowner--------------------------------------------
    def generateCiphers(self, pk, n, np,na):
        ciphers = []
        msgs = []
        for i in range(n):
            policy_str = self.getpolicy(np,na)
            msg = self.group.random(GT)
            ciphers.append(self.encrypt(policy_str, pk,msg))
            msgs.append(msg)
        return (ciphers,msgs)
        
    def encrypt(self, policy_str, pk,msg): 
        
        policy = util.createPolicy(policy_str)
        a_list = util.getAttributeList(policy)
        u = self.group.random(ZR)
        v_i = util.calculateSharesList(u, policy)
        C0 = (pk['e_gg_alpha'] ** u) * msg
    
        C1 = pk['g'] ** u
        C_i_2 = {}
        C_i_3 = {}
        C_i_4 = {}
        for i in range(len(a_list)):
            u_i = self.group.random()
            if v_i[i][0] == a_list[i]:
                j = a_list[i]
                C_i_2[j] = (pk['w'] ** v_i[i][1]) * (pk['v'] ** u_i)
                p_i = v_i[i][0].getAttribute()
                a_i = self.group.hash(p_i)
                C_i_3[j] = 1/((pk['u'] ** a_i * pk['h']) ** u_i)
                C_i_4[j] = pk['g'] ** u_i

            CT = {'C0':C0,'C1':C1,'C_i_2':C_i_2,'C_i_3':C_i_3,'C_i_4':C_i_4,'policy_str':policy_str}
        
        return CT        


    def getpolicy(self,len, MAX):
        if len == 1:
            return  str(random.randint(1,MAX))
        else:
            condition = [" or "," and "]
            r = random.randint(0,1)
            if len%2 == 0:
                return "(" + self.getpolicy(len/2,MAX) + condition[r] + self.getpolicy(len/2,MAX) + ")"
            else:
                return "(" + self.getpolicy((len-1)/2,MAX) + condition[r] + self.getpolicy((len+1)/2,MAX) + ")"
    
    def setup(self):
        g = self.group.random(G1)
        w = self.group.random(G2,1,0)
        v = self.group.random(G2)
        u = self.group.random(G2)
        h = self.group.random(G2)
        gp = self.group.random(G2)
        alpha = self.group.random(ZR)
        msk = gp ** alpha
        e_gg_alpha = pair(g,msk)
        pk = {'g':g,'w':w,'v':v,'u':u,'h':h,'e_gg_alpha':e_gg_alpha}
        # print(pk)
        return (pk, msk)

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
        for i in sk['attr']:
            tk3[i] = sk['sk_i_3'][i] ** t0
        for i in sk['attr']:
            tk4[i] = sk['sk_i_4'][i] ** t0
        dk = t0 
        tk = {'tk1':tk1,'tk2':tk2,'tk3':tk3,'tk4':tk4}
        
        return(tk, dk)

    def decrypt(self,CT_pr, dk):
        return CT_pr['C0']/(CT_pr['C_0_pr'] ** (1/dk))


def main():   
    group = ECGroup(secp384r1)
    ecdsa = ECDSA(group)
#--------------云签名秘钥------------------------- 
    secret_keystr = "0:LPemEy7v8yB8qEJrp5Vk8VVKm0mLIPspDcAuIMFwuVCvp3LCAKn8tEIjwPt5+5we"
    public_keystr = {}
    public_key = {}
    public_keystr['g'] = "1:A+w/Vl2rlRovIG3ONL/cQTZC/ZXTP4lE30d1sSCLXk9j0mQGH8hikHxE4NCSCYhPgQ=="
    public_keystr['y'] = "1:A7a9qTqQVIRm+aa1m/LPPKYvvMqp5QR+GBStCfUlA6clbf0n8jKEjl3k3Fmh7knqOw=="
    secret_key = group.deserialize(secret_keystr.encode())
    public_key['g'] = group.deserialize(public_keystr['g'].encode())
    public_key['y'] = group.deserialize(public_keystr['y'].encode())
    
    groupObj = PairingGroup('SS512')
    abeo = ABEO(groupObj)
# ----server---tcp链接----公布pk-------------
    host = '172.26.183.124'
    port = 5005
    BUFFER_SIZE = 4096  # Normally 1024, but we want fast response
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(1)
   
    conn,addr = s.accept()
    # print("conn:",conn)
    # print('Connection address:',addr)
    # print("maxsize:",s.getsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF))

    data = conn.recv(BUFFER_SIZE)
    contract_address = data.decode('utf-8')
    # print("address size:",len(data))
    conn.send("address is received".encode('utf-8'))  # echo

    data = conn.recv(BUFFER_SIZE)
    if len(data) <= 1448:
        # print(len(data))
        data += conn.recv(BUFFER_SIZE)
    
    contract_abi = pickle.loads(data)
    conn.send("abi is received".encode('utf-8'))  # echo
    
    data = conn.recv(BUFFER_SIZE)
    pkdata = pickle.loads(data)
    pk = abeo.getPk(pkdata)
    conn.send("pk is received".encode('utf-8'))  # echo

# ------dataowner-----------------------------
    
    n = 100    #密文数量
    np = 30    #policy长度
    na = 25   #属性的最大值，为了确保一定满足policy

    (ciphers, msgs) = abeo.generateCiphers(pk,n,np,na)

# -------cloud------------------------------------
    
    group = ECGroup(secp384r1)
    ecdsa = ECDSA(group)
    (public_key, secret_key) = ecdsa.keygen(0)
    public_key_send = {}
    public_key_send['g'] = group.serialize(public_key['g'])
    public_key_send['y'] = group.serialize(public_key['y'])

    
    data = conn.recv(BUFFER_SIZE)
    length = int(data.decode('utf-8'))
    conn.send("length is received".encode('utf-8'))
    
    print("length:",length)

    data = conn.recv(BUFFER_SIZE)
    while len(data) < length:
        data += conn.recv(BUFFER_SIZE)
    
    tkdata = pickle.loads(data)
    conn.send("tk is received".encode('utf-8'))  # echo
    tk = abeo.getTk(tkdata)
    # print(tk)

    data = conn.recv(BUFFER_SIZE)
    while len(data) < length:
        data += conn.recv(BUFFER_SIZE)
   
    vkdata = pickle.loads(data)
    conn.send("vk is received".encode('utf-8'))  # echo
    vk = abeo.getVk(vkdata)
    # print(vk)

    data = conn.recv(BUFFER_SIZE)
    attr_str = pickle.loads(data)
    # print(attr_str)

# --------------------首先验证秘钥的hash值--------------------
    keysstr = str(pk) + str(tk) + str(vk)
    temphash = hashlib.sha256(keysstr.encode()).hexdigest()
    w3 = Web3(Web3.HTTPProvider("http://101.76.219.50:8545"))

    cloud = w3.eth.accounts[1]
    w3.personal.unlockAccount(cloud,'') 
    # print("云账户：",cloud)
    # print("云账户余额：",w3.eth.getBalance(cloud))

    contract_instance = w3.eth.contract(address=contract_address,abi=contract_abi)
    start = time.time()
    # 从智能合约获取hash值
    tx_hash = contract_instance.functions.getkeyshash(cloud).transact(transaction={'from':cloud,'gas':44000000})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    t1 = time.time() - start

    keyshash = contract_instance.call().getkeyshash(cloud)
    if temphash != keyshash:
        print("keyshash is incorrect!!!!")
        return 
    
#----------------- 开始发送转化计算结果-----------------
    hashvalue = bytes()
    transform_verify = {}
    last = n
    wronghash = hashlib.sha256("wrong".encode()).digest()
    start = time.time()
    for i in range(n):
        CT_pr = abeo.tranform(tk,ciphers[i],attr_str)
        signature = ecdsa.sign(public_key, secret_key, str(CT_pr))
        transform_verify['c0'] = CT_pr['C_0_pr']
        CT_pr['C0'] = groupObj.serialize(CT_pr['C0'])
        CT_pr['C_0_pr'] = groupObj.serialize(CT_pr['C_0_pr'])
        # print(signature)

        signature['r'] = group.serialize(signature['r'])
        signature['s'] = group.serialize(signature['s'])
        transform = {}
        transform['CT_pr'] = CT_pr
        transform['sig'] = signature
        # 发送一个结果

        conn.send(pickle.dumps(transform))
        data = conn.recv(BUFFER_SIZE)
        if data == wronghash:
            last = i
            break
        hashvalue = data
        # print(data)
        # break
    t2 = time.time() - start
# 受到错误信号，申请矿工验证密文
    if last is not n:
        # 计算C1‘
        start = time.time()
        C_1_pr = abeo.tranform2(vk,ciphers[last],attr_str)
        
        transform_verify['c1'] = C_1_pr
        signature_verify = ecdsa.sign(public_key, secret_key, str(transform_verify))
        t1 = time.time() - start
        start = time.time()
        tx_hash = contract_instance.functions.verifyCipher(str(transform_verify) + "#",str(signature_verify) + "#",hashvalue).transact({'from':cloud,'gas':10000000})
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        t2 = time.time() - start
        print("计算c1:",t1,"cipher:",t2)
        time.sleep(3)
        print("云账户余额：",w3.eth.getBalance(cloud))

        return
    
# --------------------支付-------------------
    start = time.time()
    tx_hash = contract_instance.functions.payment(hashvalue).transact({'from':cloud,'gas':10000000})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    t3 = time.time() - start
    print("获取hash值:",t1,"交换：",t2,"支付：",t3)
    
    # print("云账户余额：",w3.eth.getBalance(cloud))

    conn.close()
    s.shutdown(SHUT_RDWR)
    s.close()
    
    return 



if __name__ == "__main__":
    main()
   
