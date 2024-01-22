from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import time

# 鍵と初期化ベクトル（IV）の生成
key = get_random_bytes(16)  # AESの鍵長は16, 24, または32バイト
iv = get_random_bytes(AES.block_size)  # AESブロックサイズに合わせたIV

# 暗号化器の生成
cipher_encrypt = AES.new(key, AES.MODE_CBC, iv)

# 暗号化するデータ（16の倍数のバイト長にする必要がある）
data = b'Your data here'
data += b' ' * (16 - len(data) % 16)  # パディング

# データの暗号化
start1 = time.time()
encrypted_data = cipher_encrypt.encrypt(data)
end1 = time.time()

# 復号化器の生成
cipher_decrypt = AES.new(key, AES.MODE_CBC, iv)

# データの復号化
start2 = time.time()
decrypted_data = cipher_decrypt.decrypt(encrypted_data)
end2 = time.time()

# パディングを取り除く
decrypted_data = decrypted_data.rstrip(b' ')

#print('Encrypted:', encrypted_data)
#print('Decrypted:', decrypted_data)

print("Enc:%f ms" % ((end1 - start1)*1000))
print("Dec:%f ms" % ((end2 - start2)*1000))
