from sshcheckers import ssh_checkout, upload_files
import yaml
import logging

logging.basicConfig(level=logging.INFO)


def load_config(file_path="config.yaml"):
    try:
        with open(file_path, encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logging.error("Конфигурационный файл не найден")
        return None
    except yaml.YAMLError:
        logging.error("Ошибка при парсинге конфигурационного файла")
        return None


def validate_config(data):
    required_keys = ["ip", "user", "passwd", "pkgname"]
    return all(key in data for key in required_keys)


def deploy(data):
    if not validate_config(data):
        logging.error("Конфигурационный файл не валиден")
        return False

    res = []
    upload_files(data["ip"], data["user"], data["passwd"], "tests/p7zip-full.deb", "/home/user2/p7zip-full.deb")

    install_cmd = f'echo {data["passwd"]} | sudo -S dpkg -i /home/user2/p7zip-full.deb'
    check_cmd = f'echo {data["passwd"]} | sudo -S dpkg -s {data["pkgname"]}'

    res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], install_cmd, "Настраивается пакет"))
    res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], check_cmd, "Status: install ok installed"))

    return all(res)


if __name__ == "__main__":
    config_data = load_config()
    if config_data and deploy(config_data):
        logging.info("Деплой успешен")
    else:
        logging.error("Ошибка деплоя")
