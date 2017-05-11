import time
import base64


def list_of_files(filename):
    with open(filename) as file:
        filelines = file.read().splitlines()
        filelist = [line.split(',') for line in filelines]
    return filelist


def encode_string(string):
    encoded_string = str(base64.urlsafe_b64encode(string.encode()))[2:-1]
    return encoded_string


def decode_file(filename):
    filelist = list_of_files(filename)
    if filename == 'answer.csv':
        for lines in filelist:
            lines[1] = time.ctime(int(lines[1]))
            lines[4] = base64.urlsafe_b64decode(str.encode(lines[4])).decode()
    elif filename == 'question.csv':
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

        
def append_to_file(filename, datalist):
    with open(filename, 'a') as file:
        for item in datalist: 
            file.write(','.join(item) + '\n')