import os

from docstash.collection import Collection
from docstash import util


class Stash(object):

    def __init__(self, path=None):
        if path is None:
            path = os.environ.get('DOCSTASH_PATH', '~/.docstash')
        path = util.fullpath(path)
        self.path = path

    def collections(self):
        if os.path.exists(self.path):
            for dir in os.listdir(self.path):
                collection = self.get(dir)
                if collection.exists():
                    yield collection

    def __iter__(self):
        return self.collections()

    def get(self, name):
        return Collection(self, name)

    def __contains__(self, name):
        collection = Collection(name)
        return collection.exists()

    def __repr__(self):
        return '<Stash(%s)>' % self.path
