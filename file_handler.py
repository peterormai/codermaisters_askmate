import time
import base64


def list_of_files(filename):
    """
    Open and read a file, then return a nested lists of the elements in the file.
    """
    with open(filename) as file:
        filelines = file.read().splitlines()
        filelist = [line.split(',') for line in filelines]
    return filelist


def encode_string(string):
    """
    Take a string as argument and return the BASE64 encrypted equivalent.
    """
    encoded_string = string.replace("\r\n", " ")
    encoded_string = " ".join(encoded_string.split())
    encoded_string = str(base64.urlsafe_b64encode(encoded_string.encode()))[2:-1]
    return encoded_string


def decode_file(filename):
    """Read file and decrypt strings from the file based on the name of the file.

        I.) If filename is "answer.csv":
            a) The fifth element of each line is going to be decrypted using BASE64.
            b) Changes currently used integer time format to a human-readable date.

        II.) If filename is "question.csv":
            a) The second and fifth element of each line is going to be decrypted using BASE64.
            b) Changes currently used integer time format to a human-readable date.

    The function returns nested lists.
    """
    filelist = list_of_files(filename)
    if filename == 'database/answer.csv':
        for lines in filelist:
            lines[1] = time.ctime(int(lines[1]))
            lines[4] = base64.urlsafe_b64decode(str.encode(lines[4])).decode()
    elif filename == 'database/question.csv':
        for lines in filelist:
            lines[1] = time.ctime(int(lines[1]))
            lines[4] = base64.urlsafe_b64decode(str.encode(lines[4])).decode()
            lines[5] = base64.urlsafe_b64decode(str.encode(lines[5])).decode()
    else:
        pass
    return filelist


def write_to_file(filename, datalist):
    with open(filename, 'w') as file:
        for item in datalist:
            file.write(','.join(item) + '\n')
