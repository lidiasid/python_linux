import os
import subprocess
import shutil
import re
import pytest

folder_out = "/home/lidiia/PycharmProjects/pythonProject/folder1"
folder_ext = "/home/lidiia/PycharmProjects/pythonProject/folder2"
file_path = f'{folder_out}/test_file.txt'

def setup_module(module):
    os.makedirs(folder_out, exist_ok=True)

    with open(file_path, 'w') as file:
        file.write("This is a test file for hashing.")

    os.system(f'7z a {folder_out}/archiv.7z {file_path}')

def teardown_module(module):
    # Удаление каталога и его содержимого после выполнения тестов
    shutil.rmtree(folder_out)

def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if text in result.stdout and result.returncode == 0:
        return True
    else:
        return False

def getout(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    return result.stdout

def test_7z_l():
    assert checkout(f'7z l {folder_out}/archiv.7z', "test_file.txt"), "test_l FAIL"

def test_7z_x():
    assert checkout(f'7z x -o{folder_ext} {folder_out}/archiv.7z', "Everything is Ok"), "test_x FAIL"

def test_7z_h():
    # Получить хеш с помощью 7z для архива
    seven_zip_hash_output = getout(f'7z h {folder_out}/archiv.7z')
    # Парсинг вывода для извлечения хеша CRC32 с помощью регулярного выражения
    match = re.search(r'CRC32 for data: ([0-9A-Fa-f]+)', seven_zip_hash_output)
    if match is None:
        raise ValueError("Failed to extract CRC32 hash from 7z output")
    seven_zip_hash = match.group(1)

    # Получить хеш с помощью crc32 для файла
    crc32_hash_output = subprocess.run(
        f'crc32 {file_path}',
        shell=True, stdout=subprocess.PIPE, encoding='utf-8'
    ).stdout.strip()
    crc32_hash = crc32_hash_output.split()[-1]

    assert seven_zip_hash == crc32_hash, f"Hash mismatch: 7z - {seven_zip_hash}, crc32 - {crc32_hash}"
