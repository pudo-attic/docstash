from os import path, makedirs
from collections import MutableMapping
from datetime import datetime

import yaml

from docstash import util


class Document(MutableMapping):

    def __init__(self, collection, content_id, **kwargs):
        self.collection = collection
        self.stash = collection.stash
        self.content_id = content_id
        self._path = None
        self._store = dict()
        self._load_meta()
        if 'created_at' not in self._store:
            self._store['created_at'] = datetime.utcnow()
        self.update(dict(**kwargs))

    @property
    def path(self):
        if self._path is None:
            prefix = path.join(self.collection.path, *self.content_id[:5])
            self._path = path.join(prefix, self.content_id)
            try:
                makedirs(self._path)
            except:
                pass
        return self._path

    @property
    def file(self):
        return path.join(self.path, self.get('file'))

    def __getitem__(self, key):
        return self._store[self.__keytransform__(key)]

    def __setitem__(self, key, value):
        self._store[self.__keytransform__(key)] = value

    def __delitem__(self, key):
        del self._store[self.__keytransform__(key)]

    def __iter__(self):
        return iter(self._store)

    def __len__(self):
        return len(self._store)

    def __keytransform__(self, key):
        return key.lower()

    def _load_meta(self):
        if path.exists(self._meta_path):
            with open(self._meta_path, 'r') as fh:
                self.update(yaml.load(fh.read()))

    def save(self):
        self._store['hash'] = self.content_id
        self._store['updated_at'] = datetime.utcnow()
        data = yaml.safe_dump(self._store,
                              canonical=False,
                              default_flow_style=False,
                              indent=4)
        with open(self._meta_path, 'w') as fh:
            fh.write(data)
            
    @property
    def _meta_path(self):
        return path.join(self.path, util.MANIFEST_FILE)

    def __repr__(self):
        return '<Document(%s, %s)>' % (self.content_id,
                                       self.get('file'))
