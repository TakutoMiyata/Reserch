import ipfshttpclient

def addToIPFS(folderName):
    # IPFSノードに接続 (デフォルトはローカルノード)
    client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')

    '''
    # 単一のファイルをアップロード
    res_file = client.add('example.txt')
    print("アップロードされたファイルのハッシュ:", res_file['Hash'])
    '''

    # フォルダ（ディレクトリ）をアップロード
    res_folder = client.add(folderName, recursive=True)

    hashes = []

    print("アップロードされたフォルダのハッシュ:")
    for file in res_folder:
        print(file['Name'], file['Hash'])
        hashes.append(file["Hash"])

    # クライアント接続を閉じる
    client.close()
    
    return hashes
if __name__ == "__main__":
    hashes = addToIPFS("otameshiFolder")
    print("Finish add to IPFS.")
    print("Saved hashes:", hashes)