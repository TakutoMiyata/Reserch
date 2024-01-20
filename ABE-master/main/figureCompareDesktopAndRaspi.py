import matplotlib.pyplot as plt
import os
import numpy as np
import csv
import pandas as pd

def main():
    df = pd.read_csv("../ExecutionTimeData/rsaTime.csv")
    rsaEncTime = df["averageEnc"]
    rsaDecTime = df["averageDec"]

    file1 = "../ExecutionTimeData/polChange.csv" 
    file2 = "../ExecutionTimeData/desktop_polChange.csv"


    # データをDataFrameに読み込む
    data1 = pd.read_csv(file1)
    data2 = pd.read_csv(file2)

    # それぞれのデータをグラフにプロット
    plt.plot(data1['lenPol'], data1['averageEnc'], label='Raspi4_Encryption', marker="o")
    plt.plot(data1['lenPol'], data1['averageDec'], label='Raspi4_Encryption', marker="o")
    plt.plot(data2['lenPol'], data2['averageEnc'], label='Desktop_Encryption', marker="o")
    plt.plot(data2['lenPol'], data2['averageDec'], label='Desktop_Decryption', marker="o")


    # グラフにタイトルとラベルを追加
    plt.title('Comparison of the time to decrypt or encrypt on Raspi4 and Desktop')
    plt.xlabel('Number of Attributes in the Policy')
    plt.ylabel('time [ms]')

    # 凡例を表示
    plt.legend()
            
    # ベクトル画像形式 (SVG) で保存
    full_path = "../ExecutionTimeData/desktopAndRaspi4.svg"
    plt.savefig(full_path, format='svg', bbox_inches='tight')
    print(f"Figure saved successfully as: {full_path}")

    print("finish")

if __name__ == "__main__":
    main()
