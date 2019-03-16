#coding=utf-8

import os
import json
from collections import defaultdict
import dateutil.parser

import config

class IndexBuilder(object):
    def __init__(self, notes):
        self.notes = notes

    def build(self):
        self.notes = self.build_doc()
        self.path_tree = self.build_path_tree()
        self.tag_tree = self.build_tag_tree()

    def dump(self):
        path_index = os.path.join(config.OUTPUT_DIR, config.PATH_INDEX)
        with open(path_index, 'w') as p:
            p.write(json.dumps(self.path_tree))

        tag_index = os.path.join(config.OUTPUT_DIR, config.TAG_INDEX)
        with open(tag_index, 'w') as t:
            t.write(json.dumps(self.tag_tree))

        for note in self.notes:
            note_path = '/'.join(note['meta']['path'])
            path = os.path.join(config.OUTPUT_DIR, config.CONTENT_PREFIX, note_path)

            self.mkdir_for_note(path)

            with open(path, 'w') as np:
                np.write(json.dumps(note))

    def mkdir_for_note(self, path):
        directory = '/'.join(path.split('/')[:-1])
        if not os.path.exists(directory):
            os.makedirs(directory)

    def build_doc(self):
        notes = []
        for note in self.notes:
            assert 'title' in note['meta']
            assert 'date' in note['meta']

            date = dateutil.parser.parse(note['meta']['date'])
            note['meta']['date'] = d.strftime('%Y-%m-%d %H:%M')

            assert 'path' in note['meta']
            assert note['meta']['path'].endswith('.md')
            path = note['meta']['path'] + '.json'

            assert 'tag' in note['meta']
            tag = note['meta']['tag']
            note['meta']['tag'] = filter(lambda x: x, map(lambda x: x.strip(), re.split('[,\n]', tag)))

            notes.append(note)
        return notes

    def build_tag_tree(self):
        tree = defaultdict(list)
        for note in self.notes:
            for tag in note['meta']['tag']:
                cur = tree
                for seg in tag.split('/'):
                    seg = seg.strip()
                    if seg not in cur:
                        cur['seg']['__meta__'] = { 'cnt' : 0 }
                    cur['seg']['__meta__']['cnt'] += 1
                    cur = cur[seg]
                cur[path[-1]] = note['meta']
        return tree

    def build_path_tree(self):
        tree = defaultdict(list)
        for note in self.notes:
            path = ['/'] + note['meta']['path'].split('/')
            cur = tree
            for seg in path[:-1]:
                if seg not in cur:
                    cur['seg']['__meta__'] = { 'cnt' : 0 }
                cur['seg']['__meta__']['cnt'] += 1
                cur = cur[seg]
            cur[path[-1]] = note['meta']
        return tree


