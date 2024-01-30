import base58

# CIDをBase58エンコードからデコード
cid_str = "QmbY17WcXxQPsF3HAomDyr64Cnp2jKesdJKiFzHzNsjV3h"
cid_bytes = base58.b58decode(cid_str)
print(cid_str)

# バイナリ対応の整数表現に変換
int_representation = int.from_bytes(cid_bytes, byteorder="big")

print(int_representation)

# バイナリ対応の整数表現からCIDバイト列に変換
int_representation = int_representation  # ここに適切な整数を設定してください
cid_bytes = int_representation.to_bytes((int_representation.bit_length() + 7) // 8, byteorder="big")

# CIDバイト列をBase58エンコード
cid_str = base58.b58encode(cid_bytes).decode('utf-8')

print(cid_str)

