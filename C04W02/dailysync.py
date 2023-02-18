#!/usr/bin/env python3

# import subprocess
# src = "/data/prod/"
# dest = "/data/prod_backup/"
# subprocess.call(["rsync", "-arq", src, dest])


import subprocess
import os
from multiprocessing import Pool

cwd = os.getcwd()


def backup(src):
    dest = cwd + '/data/prod_backup/'
    print('Backing up files from {} to {}'.format(src, dest))
    subprocess.call(["rsync", "-arq", src, dest])


def main():
    src = cwd + '/data/prod/'

    files = next(os.walk(src))[2]
    filePaths = []

    for file in files:
        filePaths.append(os.path.join(src, file))

    with Pool() as p:
        p.map(backup, filePaths)
    print("Finish.")


if __name__ == '__main__':
    main()
