import ipfshttpclient

# IPFSノードに接続 (デフォルトはローカルノード)
client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')

# 単一のファイルをアップロード
res_file = client.add('example.txt')
print("アップロードされたファイルのハッシュ:", res_file['Hash'])

# フォルダ（ディレクトリ）をアップロード
res_folder = client.add('otameshiFolder', recursive=True)
print("アップロードされたフォルダのハッシュ:")
for file in res_folder:
    print(file['Name'], file['Hash'])

# クライアント接続を閉じる
client.close()
