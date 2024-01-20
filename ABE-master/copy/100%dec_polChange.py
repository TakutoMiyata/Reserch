# charmを使ってAC17 CP-ABEを動かすコード

from charm.toolbox.pairinggroup import PairingGroup, GT
from ABE.ac17 import AC17CPABE
import time
import random
import numpy as np
import matplotlib.pyplot as plt
import os
import string
import random
import sys
import csv


def generateRandomExpression(length):
    alphabet = string.ascii_uppercase[:26]
    # Policyの数が100になるまで対応するために4倍する
    random_alphabet = ''.join(random.sample(alphabet*4, len(alphabet)*4))
    #print("Random alphabet:", random_alphabet)

    conditions = list(random_alphabet[:length])
    #print("Conditions:", conditions)

    # ランダムにANDとORを挿入
    operators = ["and", "OR"]
    for i in range(length - 1):
        # ランダムに演算子を挿入
        conditions = conditions[:1+i*2] + [random.choice(operators)] + conditions[1+i*2:]

    #print("After inserting operators:", conditions)
    #--------------------ここまでOK------------------------

    parentheses = ["(", ")"]
    num_parentheses = random.randint(1, length//3)
    #num_parentheses = 2
    #print(f"num_parentheses = {num_parentheses}")
    idx1 = np.zeros(num_parentheses)
    idx2 = np.zeros(num_parentheses)

    for j in range(num_parentheses):
        # アルファベットがある位置をランダムに選択
        alpha_positions = [pos for pos, char in enumerate(conditions) if char.isalpha() and char.isupper() and len(char) == 1]
        #print(f"alpha_positions = ", alpha_positions)
        idx1[j] = random.choice(alpha_positions)
        while idx1[j] == len(conditions) or idx1[j] == len(conditions)-1:
            idx1[j] = random.choice(alpha_positions)
        # アルファベットを囲む(を追加
        conditions = conditions[:int(idx1[j])] + [parentheses[0]] + conditions[int(idx1[j]):]
        #print("Conditions:", conditions)

    open_parentheses_positions = [pos for pos, char in enumerate(conditions) if char == "("]
    
    for k in range(num_parentheses):
        print(open_parentheses_positions)
        # アルファベットがある位置をランダムに選択
        alpha_positions = [pos for pos, char in enumerate(conditions) if char.isalpha() and char.isupper() and len(char) == 1]
        #print(f"alpha_positions = ", alpha_positions)
        idx2[k] = random.choice(alpha_positions)

        while idx2[k] == 0 or (idx2[k]-1 in open_parentheses_positions) or (conditions[int(idx2[k]-1)] == "(") or (idx2[k]-1 <= min(open_parentheses_positions)):
            idx2[k] = random.choice(alpha_positions)
            
        if idx2[k] > min(open_parentheses_positions):
            print(f"min(open_parentheses_positions) = {min(open_parentheses_positions)}")
            #indexToRemove = np.random.choice(np.where(open_parentheses_positions == np.min(open_parentheses_positions))[0]) #最小値の中から一つを選択
            #open_parentheses_positions = np.delete(open_parentheses_positions, indexToRemove) #最小値を削除
            min_positions = [i for i, pos in enumerate(open_parentheses_positions) if pos == min(open_parentheses_positions)]  # 最小値の中から一つを選択
            indexToRemove = max(min_positions)
            open_parentheses_positions.pop(indexToRemove)
            #print("最小値を削除")

        # アルファベットを囲む)を追加
        conditions = conditions[:int(idx2[k]+1)] + [parentheses[1]] + conditions[int(idx2[k]+1):]
        print("Conditions:", conditions)
    #---------------------ここまでを改善したい---------------------

    # 一番外側に()を追加
    conditions = [parentheses[0]] + conditions + [parentheses[1]]
    conditions = " ".join(map(str, conditions))
    
    #print("Final conditions:", conditions)
    #理想   Finalconditions: (A OR (B andC))...みたいな出力が欲しい
    return conditions


def figureEnc(lenPol, averageEnc):
    save_folder = "../ExecutionTimeData/"
    base_filename = "SuccessEncryption_Attribute1.svg"
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
        x = lenPol
        y = averageEnc
        plt.plot(x, y, marker="o")
        # x軸とy軸の範囲を指定（0から始まる場合）
        plt.xlim(0, max(x))
        plt.ylim(0, max(y))

        plt.title("Encryption(Attribute=1)")
        plt.xlabel("Number of Policy")
        plt.ylabel("Execution time [ms]")
        """
        plt.show()  # グラフを表示
        input("Press Enter to close...")  # Enterが押されるまで待機
        """
        # ベクトル画像形式 (SVG) で保存
        plt.savefig(full_path, format='svg', bbox_inches='tight')

        print(f"Figure saved successfully as: {full_path}")
    except Exception as e:
        print(f"Error saving figure: {e}")


def figureDec(lenPol, averageDec):
    save_folder = "../ExecutionTimeData/"
    base_filename = "SuccessDecryption_Attribute1.svg"
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
        x = lenPol
        y = averageDec
        plt.plot(x, y, marker="o")

        # x軸とy軸の範囲を指定（0から始まる場合）
        plt.xlim(0, max(x))
        plt.ylim(0, max(y))

        plt.title("Decryption(Attribute=1)")
        plt.xlabel("Number of Policy")
        plt.ylabel("Execution time [ms]")
        """
        plt.show()  # グラフを表示
        input("Press Enter to close...")  # Enterが押されるまで待機
        """
        # ベクトル画像形式 (SVG) で保存
        plt.savefig(full_path, format='svg', bbox_inches='tight')

        print(f"Figure saved successfully as: {full_path}")
    except Exception as e:
        print(f"Error saving figure: {e}")


def figureCompare(lenPol, averageEnc, averageDec):
    save_folder = "../ExecutionTimeData/"
    base_filename = "SuccessCompare_Attribute1.svg"
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
        x = lenPol
        y = averageEnc
        plt.plot(x, y, marker="o", label=("Encryption"))
        y = averageDec
        plt.plot(x, y, marker="o", label=("Decryption"))

        # x軸とy軸の範囲を指定（0から始まる場合）
        plt.xlim(0, max(x))
        plt.ylim(0, max(max(averageDec), max(averageEnc)))

        plt.title("Compare(Attribute=1)")
        plt.xlabel("Number of Policy")
        plt.ylabel("Execution time [ms]")
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
    # lenAttr = np.zeros(10)
    lenPol = np.zeros(10, dtype=int)
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
            # length = 10 + 10*m
            # attr_list = [chr(ord('A') + i % 26) for i in range(length)]
            attr_list = ["A"]
            print("attribute = ", ",".join(attr_list))
            key = cpabe.keygen(pk, msk, attr_list)

        # choose a random message
            msg = pairing_group.random(GT)

        # generate a ciphertext
            length = int(9 + 10*m)
            policy_str = generateRandomExpression(length)
            policy_str = "( " + policy_str + " OR A )"
            print("policy = ", policy_str)
            length = int (10 + 10*m)
            print(f"number of policies = {length} ")


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

        averageEnc[m] = np.mean(encTime)
        print(f"average time to Encrypt = {averageEnc[m]}")
        averageDec[m] = np.mean(decTime)
        print(f"average time to Decrypt = {averageDec[m]}")

        lenPol[m] = length

    figureEnc(lenPol, averageEnc)
    figureDec(lenPol, averageDec)
    figureCompare(lenPol, averageEnc, averageDec)

    # csvに保存
    data = list(zip(averageEnc, averageDec, lenPol))
    with open("../ExecutionTimeData/polChange.csv", "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["averageEnc", "averageDec", "lenPol"])
        csvwriter.writerows(data)
    print("Finish writing csvfile")

if __name__ == "__main__":
    debug = False
    main()


