#coding=utf-8

import markdown

class Parser(object):
    def __init__(self, input_file):
        self.input_file = input_file

    def parse(self):
        text = self.input_file.read().strip()
        md = markdown.Markdown(extensions = ['meta', 'fenced_code', 'codehilite'])
        html = md.convert(text)

        return {
            'html': html,
            'meta': md.Meta,
        }


