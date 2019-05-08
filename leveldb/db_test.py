# -*- coding: UTF-8 -*-
import unittest

from leveldb.db import LevelDB, LevelDBStatus


class LevelDBTest(unittest.TestCase):
    def test_open_close(self):
        ldb = LevelDB.open('../data/test.ldb')
        self.assertEqual(ldb.status, LevelDBStatus.OPENED)
        ldb.close()
        self.assertEqual(ldb.status, LevelDBStatus.CLOSED)

    def test_get_put(self):
        ldb = LevelDB.open('../data/test.ldb')

        ldb.put('test', 'hello')
        self.assertEqual('hello', ldb.get('test'))

        ldb.close()

    def test_read(self):
        ldb = LevelDB.open('../data/test.ldb')
        self.assertEqual('hello', ldb.get('test'))
        ldb.close()


if __name__ == '__main__':
    unittest.main()
