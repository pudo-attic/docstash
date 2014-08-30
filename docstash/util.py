from os import path
from hashlib import sha1

from werkzeug import secure_filename


MANIFEST_FILE = 'manifest.yaml'


def fullpath(filename):
    # a happy tour through stdlib
    filename = path.expanduser(filename)
    filename = path.expandvars(filename)
    filename = path.normpath(filename)
    return path.abspath(filename)


def filename(filename, default='data'):
    if filename is None:
        return filename
    basename = path.basename(filename)
    return secure_filename(basename) or default


def checksum(filename):
    hash = sha1()
    with open(filename, 'rb') as fh:
        while True:
            block = fh.read(2 ** 10)
            if not block:
                break
            hash.update(block)
    return hash.hexdigest()
