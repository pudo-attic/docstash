#
# "Bag it and tag it"
#
# Inspired by http://tools.ietf.org/html/draft-kunze-bagit-10
# At the same time, this packaging mechanism provides per-resource metadata
# (while BagIt only does checksums for each file)
#
# TODO: make this more generic so it can be on S3, too.

__all__ = ['Stash']

from docstash.stash import Stash
