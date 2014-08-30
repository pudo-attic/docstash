from docstash import Stash

# open a stash in the current working directory:
stash = Stash(path='.stash')

# print a list of collections:
print list(stash)

# access (or create) a specific collection:
collection = stash.get('test')

# import a file from the local working directory:
collection.import_file('README.md')

# iterate through each document and set a metadata
# value:
for doc in collection:
    with open(doc.file, 'rb') as fh:
        doc['body_length'] = len(fh.read())
    doc.save()
