from charm.toolbox.pairinggroup import PairingGroup, G1
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

# ペアリンググループの初期化
group = PairingGroup('SS512')

# 鍵生成: G1群のランダムな要素
key_element = group.random(G1)

# AESキーとして使用するために、鍵をバイト列に変換
raw_key = group.serialize(key_element)
# AESキーの長さを適切に調整（例：AES-256の場合は32バイト）
aes_key = raw_key[:32]

# 初期化ベクトル（IV）の生成（AESブロックサイズに合わせる）
iv = os.urandom(16)

# 暗号化（SE）関数
def encrypt(message, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    return encryptor.update(message) + encryptor.finalize()

# 復号（SD）関数
def decrypt(ciphertext, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()

# 使用例
message = b"Hello, World!"
ciphertext = encrypt(message, aes_key, iv)
plaintext = decrypt(ciphertext, aes_key, iv)

print("Original Message:", message)
print("Encrypted:", ciphertext)
print("Decrypted:", plaintext)
