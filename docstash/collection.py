from os import path, walk
import shutil

from docstash import util
from docstash.document import Document


class Collection(object):

    def __init__(self, stash, name):
        self.stash = stash
        self.name = name

    @property
    def path(self):
        return path.join(self.stash.path, self.name)

    def exists(self):
        return path.isdir(self.path)

    def documents(self):
        if self.exists():
            for (dirpath, dirnames, filenames) in walk(self.path):
                if util.MANIFEST_FILE in filenames:
                    content_id = path.basename(dirpath)
                    yield self.get(content_id)

    def get(self, content_id):
        return Document(self, content_id)

    def __iter__(self):
        return self.documents()

    def import_file(self, file_path, _move=False, **kwargs):
        file_path = util.fullpath(file_path)
        kwargs['source_path'] = file_path
        if 'file' not in kwargs:
            kwargs['file'] = util.filename(file_path)
        if 'hash' not in kwargs:
            kwargs['hash'] = util.checksum(file_path)
        doc = Document(self, kwargs['hash'], **kwargs)
        if _move:
            shutil.move(file_path, doc.file)
        else:
            shutil.copyfile(file_path, doc.file)
        doc.save()
        return doc

    def __repr__(self):
        return '<Collection(%s, %s)>' % (self.stash.path, self.name)
