# charmを使ってAC17 CP-ABEを動かすコード

from charm.toolbox.pairinggroup import PairingGroup, GT
from ABE.ac17 import AC17CPABE
import time
import random
import numpy as np
import matplotlib.pyplot as plt
import os
import csv



def figureEnc(lenAttr, averageEnc):
    save_folder = "../ExecutionTimeData/"
    base_filename = "SuccessEncryption_Policy1.svg"
    full_path = os.path.join(save_folder, base_filename)

    # ファイルが存在するか確認
    """
    count = 1
    while os.path.exists(full_path):
        # 同じ名前のファイルがある場合、新しい名前を生成
        new_filename = f"Encryption(Policy=1)_{count}.png"
        full_path = os.path.join(save_folder, new_filename)
        count += 1
    """
    try:
        plt.figure(1)
        x = lenAttr
        y = averageEnc
        plt.plot(x, y, marker="o")

        # x軸とy軸の範囲を指定（0から始まる場合）
        plt.xlim(0, max(x)*1.2)
        plt.ylim(0, max(y)*1.2)

        plt.title("Encryption(Policy=1)")
        plt.xlabel("Number of Attribute")
        plt.ylabel("Execution time [s]")
        """
        plt.show()  # グラフを表示
        input("Press Enter to close...")  # Enterが押されるまで待機
        """
        # ベクトル画像形式 (SVG) で保存
        plt.savefig(full_path, format='svg', bbox_inches='tight')

        print(f"Figure saved successfully as: {full_path}")
    except Exception as e:
        print(f"Error saving figure: {e}")


def figureDec(lenAttr, averageDec):
    save_folder = "../ExecutionTimeData/"
    base_filename = "SuccessDecryption_Policy1.svg"
    full_path = os.path.join(save_folder, base_filename)

    # ファイルが存在するか確認
    """
    count = 1
    while os.path.exists(full_path):
        
        # 同じ名前のファイルがある場合、新しい名前を生成
        new_filename = f"Decryption(Policy=1)_{count}.png"
        full_path = os.path.join(save_folder, new_filename)
        count += 1
    """
    try:
        plt.figure(2)

        x = lenAttr
        y = averageDec
        plt.plot(x, y, marker="o")

        # x軸とy軸の範囲を指定（0から始まる場合）
        plt.xlim(0, max(x)*1.2)
        plt.ylim(0, max(y)*1.2)

        plt.title("SuccessDecryption(Policy=1)")
        plt.xlabel("Number of Attribute")
        plt.ylabel("Execution time [s]")
        """
        plt.show()  # グラフを表示
        input("Press Enter to close...")  # Enterが押されるまで待機
        """
        # ベクトル画像形式 (SVG) で保存
        plt.savefig(full_path, format='svg', bbox_inches='tight')

        print(f"Figure saved successfully as: {full_path}")
    except Exception as e:
        print(f"Error saving figure: {e}")


def figureCompare(lenAttr, averageEnc, averageDec):
    save_folder = "../ExecutionTimeData/"
    base_filename = "SuccessCompare_Policy1.svg"
    full_path = os.path.join(save_folder, base_filename)

    # ファイルが存在するか確認
    """
    count = 1
    while os.path.exists(full_path):
        
        # 同じ名前のファイルがある場合、新しい名前を生成
        new_filename = f"Decryption(Policy=1)_{count}.png"
        full_path = os.path.join(save_folder, new_filename)
        count += 1
    """
    try:
        plt.figure(3)
        x = lenAttr
        y = averageEnc
        plt.plot(x, y, marker="o", label=("Encryption"))
        y = averageDec
        plt.plot(x, y, marker="o", label=("Decryption"))

        # x軸とy軸の範囲を指定（0から始まる場合）
        plt.xlim(0, max(x)*1.2)
        plt.ylim(0, max(max(averageDec), max(averageEnc))*1.2)

        plt.title("Compare(Policy=1)")
        plt.xlabel("Number of Attribute")
        plt.ylabel("Execution time [s]")
        plt.legend()
        """
        plt.show()  # グラフを表示
        input("Press Enter to close...")  # Enterが押されるまで待機
        """
        # ベクトル画像形式 (SVG) で保存
        plt.savefig(full_path, format='svg', bbox_inches='tight')

        print(f"Figure saved successfully as: {full_path}")
    except Exception as e:
        print(f"Error saving figure: {e}")


def main():
    lenAttr = np.zeros(10)
    averageEnc = np.zeros(10)
    averageDec = np.zeros(10)

    for m in range(10):
        encTime = np.zeros(10)
        decTime = np.zeros(10)

        for n in range(10):
            # instantiate a bilinear pairing map
            pairing_group = PairingGroup('MNT224')

        # AC17 CP-ABE under DLIN (2-linear)
            cpabe = AC17CPABE(pairing_group, 2)

        # run the set up
            (pk, msk) = cpabe.setup()

        # generate a key
        # ランダムな要素数を生成（例: 1から10の範囲でランダムに選択）
            # random_length = random.randint(1, 10)

        # リストを生成
            length = 9 + 10*m
            attr_list = [chr(ord('B') + i % 25) for i in range(length)]
            attr_list.append("A")
            print("attribute = ", ",".join(attr_list))
            key = cpabe.keygen(pk, msk, attr_list)

        # choose a random message
            msg = pairing_group.random(GT)

        # generate a ciphertext
            policy_str = 'A'
            print("policy = ", policy_str)

        # encryption
            start_time = time.time()  # 計測開始

            ctxt = cpabe.encrypt(pk, msg, policy_str)

            end_time = time.time()  # 計測終了
            encTime[n] = end_time - start_time  # 実行時間の計算
            print(f"execution time to Encrypt = {encTime[n]}")

        # decryption
            start_time = time.time()  # 計測開始

            rec_msg = cpabe.decrypt(pk, ctxt, key)

            end_time = time.time()  # 計測終了
            decTime[n] = end_time - start_time  # 実行時間の計算
            print(f"execution time to Decrypt = {decTime[n]}")

        # if debug:
            if rec_msg == msg:
                print("Successful decryption.")
            else:
                print("Decryption failed.")
                sys.exit()

            line = '-' * 20  # 20回のハイフンで構成された文字列
            print("\n" + line + "\n")

        lenAttr[m] = len(attr_list)
        print(f"number of attributes = {int(lenAttr[m])} ")
        averageEnc[m] = np.mean(encTime)
        print(f"average time to Encrypt = {averageEnc[m]}")
        averageDec[m] = np.mean(decTime)
        print(f"average time to Decrypt = {averageDec[m]}")

    figureEnc(lenAttr, averageEnc)
    figureDec(lenAttr, averageDec)
    figureCompare(lenAttr, averageEnc, averageDec)

    # csvに保存
    data = list(zip(averageEnc, averageDec, lenAttr))
    with open("../ExecutionTimeData/attrChange.csv", "w", newline="") as csvfile:
        try:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["averageEnc", "averageDec", "lenAttr"])
            csvwriter.writerows(data)
            print("Finish writing csvfile")
        except Exception as e:
            print(f"Error wrting csvfile: {e}")


if __name__ == "__main__":
    debug = False
    main()

