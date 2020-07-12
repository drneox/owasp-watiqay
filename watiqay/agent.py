from os import walk
from sys import argv
import hashlib


def integrity_monitor(PROTECT_PATH):
    files_dict = {}
    for base, dirs, files in walk(PROTECT_PATH):
        for file in files:
            archive = base + '/' + file
            with open(archive, 'rb') as file:
                content = file.read()
            sha256 = hashlib.sha256(content)
            hash = sha256.hexdigest()
            files_dict[archive.replace('.', '__')] = str(hash)
    data = {}
    for key, value in files_dict.items():
        data[key] = value
    print(data)
    return data


if __name__ == '__main__':
    integrity_monitor(argv[1])
