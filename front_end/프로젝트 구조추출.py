# list_py_files.py
import os

def list_py_files(start_path):
    structure = []
    for root, dirs, files in os.walk(start_path):
        # venv 폴더 제외
        if 'venv' in root:
            continue
            
        # .py 파일만 필터링
        py_files = [f for f in files if f.endswith('.py')]
        if py_files:
            rel_path = os.path.relpath(root, start_path)
            if rel_path == '.':
                rel_path = ''
            for py_file in py_files:
                full_path = os.path.join(rel_path, py_file)
                structure.append(full_path)
    
    return sorted(structure)

if __name__ == '__main__':
    # 현재 디렉토리를 기준으로 시작
    files = list_py_files('.')
    for file in files:
        print(file)