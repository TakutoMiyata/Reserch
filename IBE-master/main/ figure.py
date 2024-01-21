import matplotlib.pyplot as plt
import os
import numpy as np
import csv
import pandas as pd

def figure(fileName):
    df = pd.read_csv(fileName)
    full_path = "../ExecutionTimeData/figureCompare.svg"

    try:# ABEそのままIBE用に変更すること！
        plt.figure(1)
        plt.plot(df['lenPol'], df['averageEnc'], label='ABE Encyiption', marker="o")
        plt.plot(df['lenPol'], df['averageDec'], label='ABE Decryption', marker="o")
        
        # RSA Encryptionの水平線
        plt.axhline(rsaEncTime.iloc[0], color="r", linestyle='--', label='RSA Encryption')  # RSAの場合の値
        # テキスト表示
        plt.text(0, rsaEncTime.iloc[0], f'RSA Encryption: {rsaEncTime.iloc[0]:.6f}', color="r")

        # RSA Decryptionの水平線
        plt.axhline(rsaDecTime.iloc[0], color="g", linestyle='--', label='RSA Decryption')  # RSAの場合の値
        # テキスト表示
        plt.text(0, rsaDecTime.iloc[0], f'RSA Decryption: {rsaDecTime.iloc[0]:.6f}', color="g")

        # x軸とy軸の範囲を指定（0から始まる場合）
        plt.xlim(0, max(df['lenPol'])*1.2)
        plt.ylim(0, max(max(df['averageDec']), max(df['averageEnc']))*1.2)

        plt.xlabel("Number of Attributes in the Policy")
        plt.ylabel("Execution time [s]")
        plt.legend()


        # ベクトル画像形式 (SVG) で保存
        plt.savefig(full_path, format='svg', bbox_inches='tight')
        print(f"Figure saved successfully as: {full_path}")
    except Exception as e:
        print(f"Error saving figure: {e}")
