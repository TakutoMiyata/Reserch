import os
import shutil

def empty_folder(folder_path):
    """指定されたフォルダの中身を空にする。
    
    Args:
        folder_path (str): 空にするフォルダのパス。
    """
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.remove(item_path)  # ファイルまたはシンボリックリンクを削除
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)  # ディレクトリを削除

