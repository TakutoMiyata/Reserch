import rsa
import time
import numpy as np
import csv

encTime = np.zeros(10)
decTime = np.zeros(10)

for n in range(10):
    # 鍵の生成
    (bits, e, d) = 1024, 65537, None  # ビット数、公開指数、秘密指数
    (public_key, private_key) = rsa.newkeys(bits, poolsize=8)

    # 鍵の保存
    with open("private_key.pem", "wb") as f:
        f.write(private_key.save_pkcs1())

    with open("public_key.pem", "wb") as f:
        f.write(public_key.save_pkcs1())

    # メッセージの準備
    message = b"Hello, RSA!"

    # メッセージの暗号化
    start_time = time.time()  # 計測開始
    ciphertext = rsa.encrypt(message, public_key)
    end_time = time.time()  # 計測終了
    encTime[n] = end_time - start_time  # 実行時間の計算
    print(f"execution time to Encrypt = {encTime[n]}")

    # 暗号文の表示
    print("Ciphertext:", ciphertext)

    # 復号
    start_time = time.time()  # 計測開始
    decrypted_message = rsa.decrypt(ciphertext, private_key)
    end_time = time.time()  # 計測終了
    decTime[n] = end_time - start_time  # 実行時間の計算
    print(f"execution time to Decrypt = {decTime[n]}")

    # 復号結果の表示
    print("Decrypted Message:", decrypted_message.decode("utf-8"))

line = '-' * 20  # 20回のハイフンで構成された文字列
print("\n" + line + "\n")

averageEnc = np.mean(encTime)
print(f"average time to Encrypt = {averageEnc}")
averageDec = np.mean(decTime)
print(f"average time to Decrypt = {averageDec}")

# NumPy配列からリストに変換
data = [averageEnc.item(), averageDec.item()]

with open("../ExecutionTimeData/rsaTime.csv", "w", newline="") as csvfile:
    try:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["averageEnc", "averageDec"])
        csvwriter.writerows([data])  # リストのリストに変更
        print("Finish writing csvfile")
    except Exception as e:
        print(f"Error writing csvfile: {e}")
