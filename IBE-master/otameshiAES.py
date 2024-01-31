from Crypto.Cipher import AES
from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair, extract_key

# プレーンテキストデータ
plaintext = b'This is a secret message'
group = PairingGroup("MNT159")
g = group.random(ZR)
# 対称キーの抽出
symmetric_key = extract_key(g)

# AES暗号化オブジェクトの作成
cipher = AES.new(symmetric_key, AES.MODE_EAX)

# データの暗号化
ciphertext, tag = cipher.encrypt_and_digest(plaintext)

# 復号化オブジェクトの作成
cipher = AES.new(symmetric_key, AES.MODE_EAX, nonce=cipher.nonce)

# データの復号化
decrypted_data = cipher.decrypt(ciphertext)

print("暗号化されたデータ:", ciphertext)
print("復号化されたデータ:", decrypted_data)
