from os import path, makedirs
from collections import MutableMapping
from datetime import datetime
from lockfile import FileLock

import yaml

from docstash import util


class Document(MutableMapping):

    def __init__(self, collection, content_id, **kwargs):
        self.collection = collection
        self.stash = collection.stash
        self.content_id = content_id
        self._path = None
        self.meta = dict()
        self._meta_lock = FileLock(self._meta_path)
        self._load_meta()
        if 'created_at' not in self.meta:
            self.meta['created_at'] = datetime.utcnow()
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
        return self.meta[self.__keytransform__(key)]

    def __setitem__(self, key, value):
        self.meta[self.__keytransform__(key)] = value

    def __delitem__(self, key):
        del self.meta[self.__keytransform__(key)]

    def __contains__(self, key):
        return self.__keytransform__(key) in self.meta

    def __iter__(self):
        return iter(self.meta)

    def __len__(self):
        return len(self.meta)

    def __keytransform__(self, key):
        return key.lower()

    def _load_meta(self):
        try:
            if path.exists(self._meta_path):
                with open(self._meta_path, 'r') as fh:
                    with self._meta_lock:
                        self.update(yaml.load(fh.read()))
        except (ValueError, TypeError):
            pass

    def save(self):
        self._meta_lock.acquire()
        self.meta['hash'] = self.content_id
        self.meta['updated_at'] = datetime.utcnow()
        data = yaml.safe_dump(self.meta,
                              canonical=False,
                              default_flow_style=False,
                              indent=4)
        with open(self._meta_path, 'w') as fh:
            with self._meta_lock:
                fh.write(data)
            
    @property
    def _meta_path(self):
        return path.join(self.path, util.MANIFEST_FILE)

    def __repr__(self):
        return '<Document(%s, %s)>' % (self.content_id,
                                       self.get('file'))
