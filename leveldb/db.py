# -*- coding: UTF-8 -*-
import pickle

from whistle import EventDispatcher

LINE_SEPARATOR = bytes('\n', 'utf-8')


def serialize(obj):
    return pickle.dumps(obj) + LINE_SEPARATOR


def deserialize(b):
    b.strip(LINE_SEPARATOR)
    return pickle.loads(b)


class LevelDBStatus:
    OPENED = 1
    CLOSED = 2


class LevelDB(EventDispatcher):
    status = None

    def __init__(self, file, options):
        super().__init__()

        self.file = file
        self._conf = options

        self.lines = dict()
        self.init()
        self.current_pos = self.file.tell()

        self.buffer = dict()

        self.add_listener('flush', self.do_flush)

        self.status = LevelDBStatus.OPENED

    @classmethod
    def open(cls, file_name, options=None):
        file = open(file_name, 'a+b')
        return cls(file, options)

    def init(self):
        for line in self.file:
            print(line)
            self.lines.update(deserialize(line))

    def get(self, key):
        return self.buffer.get(key) or self.lines.get(key)

    def put(self, key, value):
        self.buffer[key] = value

    def do_flush(self):
        self.lines.update(self.buffer)
        buffer = []
        for (k, v) in self.buffer.items():
            buffer.append(serialize({k: v}))
        self.file.writelines(buffer)
        self.buffer.clear()

    def close(self):
        self.status = LevelDBStatus.CLOSED
        self.do_flush()
        self.file.close()
