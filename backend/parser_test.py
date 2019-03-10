#coding=utf-8

import pytest
from parser import Parser

class FileStub(object):
    def __init__(self, content):
        self.content = content

    def read(self):
        return self.content

def test_parser_basic():
    f = FileStub('''\
---
title: hello world
tags: foo, bar, a/b/c, 1/2/3/4/5
---

# H1

## H2

### H3

```html
<a href="#">My code</a>
```

```python
print 'hello world'
```



**BOLD**
''')

    p = Parser(f)
    res = p.parse()


    assert res['meta']
    assert res['meta']['title'] == ['hello world']
    assert 'foo' in res['meta']['tags'][0]
    assert 'python' not in res['html']
    assert '<h1>H1</h1>' in res['html']
