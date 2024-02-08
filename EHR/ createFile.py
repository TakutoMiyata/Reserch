import os

def create_text_file(filename, size_in_bytes, text="A"):
    """指定されたサイズのテキストファイルを生成する。
    
    Args:
        filename (str): 生成するファイルの名前。
        size_in_bytes (int): ファイルのサイズ（バイト単位）。
        text (str): ファイルに書き込むテキスト。
    """
    with open(filename, 'w') as f:
        # 書き込むテキストのサイズを計算
        text_length = len(text)
        # 指定されたサイズに達するまでテキストを繰り返し書き込む
        for _ in range(size_in_bytes // text_length):
            f.write(text)
        # 最後の部分でサイズが合わない場合に残りを埋める
        f.write(text[:size_in_bytes % text_length])

# 例: "ExampleText"を繰り返し含む1MB（約1048576バイト）のファイルを生成
create_text_file("fileSize/1kbFile.txt", 1024, "ExampleText")
create_text_file("fileSize/10kbFile.txt", 1024*2, "ExampleText")

