import matplotlib.pyplot as plt
import os
import numpy as np
import csv
import pandas as pd

def figurePol(fileName, rsaEncTime, rsaDecTime):
    df = pd.read_csv(fileName)
    full_path = "figurePolChange.svg"

    try:
        plt.figure(1)
        plt.plot(df['lenPol'], df['averageEnc'], label='ABE Encyiption', marker="o")
        plt.plot(df['lenPol'], df['averageDec'], label='ABE Decryption', marker="o")
        plt.axhline(rsaEncTime.iloc[0], label='RSA Encryption')  # RSAの場合の値
        plt.axhline(rsaDecTime.iloc[0], label='RSA Decryption')  # RSAの場合の値
        plt.legend()

        # x軸とy軸の範囲を指定（0から始まる場合）
        plt.xlim(0, max(df['lenPol']))
        plt.ylim(0, max(max(df['averageDec']), max(df['averageEnc'])))

        plt.xlabel("Number of Policies")
        plt.ylabel("Execution time [ms]")

        # ベクトル画像形式 (SVG) で保存
        plt.savefig(full_path, format='svg', bbox_inches='tight')
        print(f"Figure saved successfully as: {full_path}")
    except Exception as e:
        print(f"Error saving figure: {e}")

def figureAttr(fileName, rsaEncTime, rsaDecTime):
    df = pd.read_csv(fileName)
    full_path = "figureAttrChange.svg"

    try:
        plt.figure(2)
        plt.plot(df['lenAttr'], df['averageEnc'], label='Encyiption', marker="o")
        plt.plot(df['lenAttr'], df['averageDec'], label='Decryption', marker="o")
        plt.axhline(rsaEncTime.iloc[0], color = "r", label='RSA Encryption')  # RSAの場合の値
        plt.axhline(rsaDecTime.iloc[0], color = "g", label='RSA Decryption')  # RSAの場合の値
        plt.legend()

        # x軸とy軸の範囲を指定（0から始まる場合）
        plt.xlim(0, max(df['lenAttr']))
        plt.ylim(0, max(max(df['averageDec']), max(df['averageEnc'])))

        plt.xlabel("Number of Attributes")
        plt.ylabel("Execution time [ms]")

        # ベクトル画像形式 (SVG) で保存
        plt.savefig(full_path, format='svg', bbox_inches='tight')
        print(f"Figure saved successfully as: {full_path}")
    except Exception as e:
        print(f"Error saving figure: {e}")

def main():
    df = pd.read_csv("../ExecutionTimeData/rsaTime.csv")
    rsaEncTime = df["averageEnc"]
    rsaDecTime = df["averageDec"]

    fileName ="polChange.csv" 
    figurePol(fileName, rsaEncTime, rsaDecTime)

    fileName = "attrChange.csv" 
    figureAttr(fileName, rsaEncTime, rsaDecTime)

    print("finish")

if __name__ == "__main__":
    main()
