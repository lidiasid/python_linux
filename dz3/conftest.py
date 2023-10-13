import pytest
import yaml
import random
import string
from datetime import datetime
from chekers import checkout
from chekers import getout
from datetime import datetime

with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def make_folders():
    return checkout(
        "mkdir {} {} {} {}".format(data["folder_in"], data["folder_out"], data["folder_ext"],
                                   data["folder_ext2"]), "")


@pytest.fixture()
def clear_folders():
    return checkout("rm -rf {}/* {}/* {}/* {}/*".format(data["folder_in"], data["folder_out"],
                                                        data["folder_ext"], data["folder_ext2"]), "")


@pytest.fixture()
def make_files():
    list_of_files = []
    for i in range(data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if checkout("cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["folder_in"],
                                                                                           filename, data["bs"]), ""):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not checkout("cd {}; mkdir {}".format(data["folder_in"], subfoldername), ""):
        return None, None
    if not checkout(
            "cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data["folder_in"],
                                                                                      subfoldername, testfilename), ""):
        return subfoldername, None
    else:
        return subfoldername, testfilename


@pytest.fixture(autouse=True)
def print_time():
    yield print("Start: {}".format(datetime.now().strftime("%H:%M:%S.%f")))
    print("Finish: {}".format(datetime.now().strftime("%H:%M:%S.%f")))


# Задание 1.
# Дополнить проект фикстурой, которая после каждого шага теста дописывает в заранее созданный файл stat.txt
# строку вида: время, кол-во файлов из конфига, размер файла из конфига, статистика загрузки процессора из
# файла /proc/loadavg (можно писать просто всё содержимое этого файла).

def write_stat():
    with open('config.yaml') as f:
        config_data = yaml.safe_load(f)
    num_files = config_data['count']
    file_size = config_data['bs']
    with open('/proc/loadavg', 'r') as f:
        load_avg = f.read().strip()
    with open('stat.txt', 'a') as f:  # 'a' означает append, файл будет создан, если он не существует
        f.write(f'{datetime.now()}, {num_files}, {file_size}, {load_avg}\n')

@pytest.fixture(autouse=True)
def stat_report(request):
    def write_stat():
        with open('config.yaml') as f:
            config_data = yaml.safe_load(f)
        num_files = config_data['count']
        file_size = config_data['bs']
        with open('/proc/loadavg', 'r') as f:
            load_avg = f.read().strip()
        with open('stat.txt', 'a') as f:
            f.write(f'{datetime.now()}, {num_files}, {file_size}, {load_avg}\n')

    request.addfinalizer(write_stat)


