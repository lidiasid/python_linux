import subprocess
import string


def test_command(command, text, split_mode=False):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True, encoding='utf-8')
    output = result.stdout

    if split_mode:
        translator = str.maketrans('', '', string.punctuation)
        output = output.translate(translator)
        words = output.split()
        return text in words

    return text in output


command = 'ls -l'
text = 'texttxt'
is_successful = test_command(command, text, split_mode=True)
print(is_successful)
