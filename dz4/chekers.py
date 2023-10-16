import yaml
import pytest
from sshcheckers import ssh_checkout, upload_files, ssh_getout


class TestPositive:

    @pytest.fixture(scope='class', autouse=True)
    def setup_data(self):
        with open('config.yaml') as fy:
            self.data = yaml.safe_load(fy)

    def save_log(self, start_time, name):
        with open(name, 'a') as f:
            f.write(ssh_getout(self.data["ip"], self.data["user"], self.data["passwd"],
                               f"journalctl --since '{start_time}'"))

    def common_ssh_checkout(self, command, check_text):
        return ssh_checkout(self.data["ip"], self.data["user"], self.data["passwd"], command, check_text)

    def test_deploy(self):
        start_time = "2023-10-15 12:00:00"
        res = []

        res.append(self.common_ssh_checkout('ls /opt', 'dir1'))
        res.append(self.common_ssh_checkout('ls /usr', 'bin'))

        upload_files(self.data["ip"], self.data["user"], self.data["passwd"], '/localpath/to/file',
                     '/remotepath/to/file')

        res.append(self.common_ssh_checkout('ls /remotepath/to', 'file'))

        self.save_log(start_time, "log_positive.txt")

        assert all(res), "test_deploy FAIL"

    def test_service(self):
        start_time = "2023-10-15 12:30:00"
        res = []

        res.append(self.common_ssh_checkout('systemctl status sshd', 'active (running)'))

        self.save_log(start_time, "log_positive.txt")

        assert all(res), "test_service FAIL"
