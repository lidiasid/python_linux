import pytest
from sshcheckers import ssh_checkout, ssh_checkout_negative, ssh_getout, upload_files
import yaml
from datetime import datetime


@pytest.fixture(scope='module')
def config():
    with open('config.yaml') as f:
        return yaml.safe_load(f)


@pytest.fixture(scope='function')
def start_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class TestNegative:

    @staticmethod
    def save_log(start_time, name, config):
        with open(name, 'a') as f:
            f.write(ssh_getout(config["ip"], config["user"], config["passwd"], f"journalctl --since '{start_time}'"))

    def test_deploy(self, start_time, config):
        res = []
        upload_files(config["ip"], config["user"], config["passwd"], f'tests/{config["pkgname"]}.deb',
                     f'/home/{config["user"]}/{config["pkgname"]}.deb')
        res.append(ssh_checkout(config["ip"], config["user"], config["passwd"],
                                f'echo "{config["passwd"]}" | sudo -S dpkg -i /home/{config["user"]}/{config["pkgname"]}.deb',
                                "Настраивается пакет"))
        res.append(ssh_checkout(config["ip"], config["user"], config["passwd"],
                                f'echo "{config["passwd"]}" | sudo -S dpkg -s {config["pkgname"]}',
                                "Status: install ok installed"))
        self.save_log(start_time, "log_negative.txt", config)
        assert all(res), "test_deploy FAIL"

    def test_negative1(self, make_folder, clear_folder, make_files, create_bad_archive, start_time, config):
        self.save_log(start_time, "log_negative.txt", config)
        assert ssh_checkout_negative(config["ip"], config["user"], config["passwd"],
                                     f'cd {config["folder_bad"]}; 7z e arx2.{config["arc_type"]} -o{config["folder_ext"]} -y',
                                     "ERRORS")

    def test_negative2(self, make_folder, clear_folder, make_files, create_bad_archive, start_time, config):
        self.save_log(start_time, "log_negative.txt", config)
        assert ssh_checkout_negative(config["ip"], config["user"], config["passwd"],
                                     f'cd {config["folder_bad"]}; 7z t arx2.{config["arc_type"]}',
                                     "Is not")


if __name__ == '__main__':
    pytest.main(['-v'])
