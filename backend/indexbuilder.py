#coding=utf-8

import config
from collections import defaultdict
import dateutil.parser

class IndexBuilder(object):
    def __init__(self, notes):
        self.notes = notes

    def build(self):
        self.notes = self.build_doc()
        self.path_tree = self.build_path_tree()
        self.tag_tree = self.build_tag_tree()

    def dump(self):
        pass

    def build_doc(self):
        notes = []
        for note in self.notes:
            assert 'title' in note['meta']
            assert 'date' in note['meta']

            date = dateutil.parser.parse(note['meta']['date'])
            note['meta']['date'] = d.strftime('%Y-%m-%d %H:%M')

            assert 'path' in note['meta']
            path = note['meta']['path']
            note['meta']['path'] = ['/'] + filter(lambda x: x, 
                    map(lambda s: s.strip(), path.split('/')))

            assert 'tag' in note['meta']
            tag = note['meta']['tag']
            note['meta']['tag'] = ['/'] + filter(lambda x: x, 
                    map(lambda s: s.strip(), tag.split('/')))
            notes.append(note)
        return notes

    def build_tree(self, extractor):
        tree = defaultdict(list)
        for note in self.notes:
            path = extractor(note)
            cur = tree['/']
            cur.append(note)
            for seg in path:
                cur = cur[seg]
                cur.append(note)
        return tree

    def build_tag_tree(self):
        return self.build_tree(lambda note: note['meta']['tags'])

    def build_path_tree(self):
        return self.build_tree(lambda note: note['meta']['path'])




