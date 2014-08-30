from os import path
from hashlib import sha1
from httplib import HTTPResponse
from urllib2 import urlopen
from StringIO import StringIO
from urlparse import urlparse

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


def clean_headers(headers):
    result = {}
    for k, v in dict(headers).items():
        k = k.lower().replace('-', '_')
        result[k] = v
    return result


def ingest_misc(coll, obj, **kwargs):

    if isinstance(obj, basestring):
        # Treat strings as paths or URLs
        url = urlparse(obj)
        if url.scheme.lower() in ['http', 'https']:
            try:
                import requests
                obj = requests.get(obj)
            except ImportError:
                obj = urlopen(obj)
        elif url.scheme.lower() in ['file', '']:
            if path.isdir(url.path):
                return coll.ingest_dir(url.path)
            return coll.ingest_file(url.path)
    
    # Python requests
    try:
        from requests import Response
        if isinstance(obj, Response):
            kwargs['source_status'] = obj.status_code
            kwargs['headers'] = clean_headers(obj.headers)
            kwargs['source_url'] = obj.url
            kwargs['file'] = obj.url
            fd = StringIO(obj.content)
            return coll.ingest_fileobj(fd, **kwargs)
    except ImportError:
        pass

    if isinstance(obj, HTTPResponse):
        # Can't tell the URL for HTTPResponses
        kwargs['source_status'] = obj.status
        # TODO handle lists:
        kwargs['headers'] = clean_headers(obj.getheaders())
        return coll.ingest_fileobj(obj, **kwargs)
    elif hasattr(obj, 'geturl') and hasattr(obj, 'info'):
        # assume urllib or urllib2
        kwargs['source_url'] = obj.url
        kwargs['file'] = obj.url
        kwargs['source_status'] = obj.getcode()
        kwargs['headers'] = clean_headers(obj.headers)
        return coll.ingest_fileobj(obj, **kwargs)
    elif hasattr(obj, 'read'):
        # Fileobj will be a bit bland
        return coll.ingest_fileobj(obj, **kwargs)

    raise ValueError("Can't ingest: %r" % obj)







