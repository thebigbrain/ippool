# -*- coding: UTF-8 -*-
from whistle import EventDispatcher


class LevelDB(EventDispatcher):
    def __init__(self, file, options):
        super().__init__()

        self.file = file
        self._conf = options

        self.lines = self.file.readlines()

        self.buffer = []

        self.current_pos = self.file.tell()

        self.add_listener('flush', self.on_flush)

    @classmethod
    def open(cls, file_name, options):
        file = open(file_name, 'ra')
        return cls(file, options)

    def get(self, key):
        return ''

    def put(self, key, value):
        pass

    def on_flush(self):
        pass

    def close(self):
        self.file.close()
