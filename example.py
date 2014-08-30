from docstash import Stash

# open a stash in the current working directory:
stash = Stash(path='.stash')

# print a list of collections:
print list(stash)

# access (or create) a specific collection:
collection = stash.get('test')

# import a file from the local working directory:
collection.ingest('README.md')

# import an http resource:
collection.ingest('http://pudo.org/index.html')

#collection.ingest_dir('.')

# iterate through each document and set a metadata
# value:
for doc in collection:
    print doc
    with open(doc.file, 'rb') as fh:
        doc['body_length'] = len(fh.read())
    doc.save()
