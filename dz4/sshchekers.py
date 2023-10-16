import paramiko
import yaml

def create_ssh_client(host, user, passwd, port=22):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=user, password=passwd, port=port)
        return client
    except Exception as e:
        print(f"Failed to connect: {e}")
        return None

def exec_ssh_command(client, cmd):
    try:
        stdin, stdout, stderr = client.exec_command(cmd)
        exit_code = stdout.channel.recv_exit_status()
        out = (stdout.read() + stderr.read()).decode("utf-8")
        return exit_code, out
    except Exception as e:
        print(f"Failed to execute command: {e}")
        return None, None

def ssh_checkout(host, user, passwd, cmd, text, port=22):
    client = create_ssh_client(host, user, passwd, port)
    if client:
        exit_code, out = exec_ssh_command(client, cmd)
        client.close()
        return text in out and exit_code == 0
    return False

def upload_files(host, user, passwd, local_path, remote_path, port=22):
    try:
        print(f"Uploading file {local_path} to directory {remote_path}")
        transport = paramiko.Transport((host, port))
        transport.connect(None, username=user, password=passwd)
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put(local_path, remote_path)
        sftp.close()
        transport.close()
    except Exception as e:
        print(f"Failed to upload file: {e}")

def ssh_getout(host, user, passwd, cmd, port=22):
    client = create_ssh_client(host, user, passwd, port)
    if client:
        exit_code, out = exec_ssh_command(client, cmd)
        client.close()
        return out
    return ""

def ssh_checkout_negative(host, user, passwd, cmd, text, port=22):
    client = create_ssh_client(host, user, passwd, port)
    if client:
        exit_code, out = exec_ssh_command(client, cmd)
        client.close()
        return text in out and exit_code != 0
    return False

if __name__ == "__main__":
    with open('config.yaml') as fy:
        data = yaml.safe_load(fy)
    upload_files(data["ip"], data["user"], data["passwd"], "/path/to/local/file", "/path/to/remote/file")
