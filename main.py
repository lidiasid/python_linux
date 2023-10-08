
import subprocess

def test_command(command, text):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True, encoding='utf-8')
    return text in result.stdout
command = 'ls -l'
text = 'text.txt'
is_successful = test_command(command, text)
print(is_successful)



