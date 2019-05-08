# -*- coding: UTF-8 -*-
import os
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


class LevelDBEvent:
    FLUSH = 'flush'


class LevelDB(EventDispatcher):
    status = None

    def __init__(self, file, options):
        super().__init__()

        self.file = file
        self._conf = options

        self.lines = dict()
        self.current_pos = 0
        self.init()

        self.buffer = dict()

        self.add_listener(LevelDBEvent.FLUSH, self.do_flush)

        self.status = LevelDBStatus.OPENED

    @classmethod
    def open(cls, file_name, options=None):
        file = open(file_name, 'a+b')
        return cls(file, options)

    def init(self):
        self.file.seek(os.SEEK_SET)
        for line in self.file:
            self.current_pos += 1
            self.lines.update(deserialize(line))

    def get(self, key):
        return self.buffer.get(key) or self.lines.get(key)

    def put(self, key, value):
        self.buffer[key] = value
        if len(self.buffer.items()) > 10:
            self.dispatch(LevelDBEvent.FLUSH)

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
