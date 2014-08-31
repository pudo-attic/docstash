from os import path, walk, close, unlink
from tempfile import mkstemp
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

    def ingest(self, something, _move=False, **kwargs):
        return util.ingest_misc(self, something, _move=_move, **kwargs)

    def ingest_fileobj(self, file_obj, _move=False, **kwargs):
        if 'file' not in kwargs:
            kwargs['file'] = None
        sysfd, path = mkstemp()
        with open(path, 'wb') as fh:
            fh.write(file_obj.read())
        close(sysfd)
        return self.ingest_file(path, _move=True, **kwargs)

    def ingest_file(self, file_path, _move=False, **kwargs):
        file_path = util.fullpath(file_path)
        if not _move:
            kwargs['source_path'] = file_path
        file_name = kwargs.get('file', file_path)
        kwargs['file'] = util.filename(file_name)
        if 'hash' not in kwargs:
            kwargs['hash'] = util.checksum(file_path)
        doc = Document(self, kwargs['hash'], **kwargs)
        if file_path != doc.file:
            if not path.exists(doc.file):
                if _move:
                    shutil.move(file_path, doc.file)
                else:
                    shutil.copyfile(file_path, doc.file)
            elif _move:
                unlink(file_path)
        doc.save()
        return doc

    def ingest_dir(self, dir_path, **kwargs):
        for (dirpath, dirnames, file_names) in walk(dir_path):
            for file_name in file_names:
                file_path = path.join(dirpath, file_name)
                self.import_file(file_path, **kwargs)

    def __repr__(self):
        return '<Collection(%s, %s)>' % (self.stash.path, self.name)
