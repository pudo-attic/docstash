from os import path, listdir

from docstash.collection import Collection

            
class Stash(object):

    def __init__(self, path):
        self.path = path

    def collections(self):
        if path.exists(self.path):
            for dir in listdir(self.path):
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
