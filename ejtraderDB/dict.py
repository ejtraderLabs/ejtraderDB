#! coding = utf-8
import logging
import sqlite3

from ejtraderDB import sqlite_set 

log = logging.getLogger(__name__)


class DictSQLite(sqlite_set.SQLiteSet, dict):
    _TABLE_NAME = 'dict'
    _KEY_COLUMN = 'key'
    _SQL_CREATE = ('CREATE TABLE IF NOT EXISTS {table_name} ('
                   '{key_column} TEXT PRIMARY KEY, data BLOB)')
    _SQL_INSERT = 'INSERT INTO {table_name} (key, data) VALUES (?, ?)'
    _SQL_SELECT = ('SELECT {key_column}, data FROM {table_name} '
                   'WHERE {key_column} = ?')
    _SQL_UPDATE = 'UPDATE {table_name} SET data = ? WHERE {key_column} = ?'

    def __init__(self, path=None, name=None, multithreading=True,auto_commit=True):
        # PDict is always auto_commit=True
        super(DictSQLite, self).__init__(path, name=name,
                                    multithreading=multithreading,
                                    auto_commit=auto_commit)

    def __iter__(self):
        raise NotImplementedError('Not supported.')

    def keys(self):
        raise NotImplementedError('Not supported.')

    def iterkeys(self):
        raise NotImplementedError('Not supported.')

    def values(self):
        raise NotImplementedError('Not supported.')

    def itervalues(self):
        raise NotImplementedError('Not supported.')

    def iteritems(self):
        raise NotImplementedError('Not supported.')

    def items(self):
        raise NotImplementedError('Not supported.')

    def __contains__(self, item):
        row = self._select(item)
        return row is not None

    def __setitem__(self, key, value):
        obj = self._serializer.dumps(value)
        try:
            self._insert_into(key, obj)
        except sqlite3.IntegrityError:
            self._update(key, obj)

    def __getitem__(self, item):
        row = self._select(item)
        if row:
            return self._serializer.loads(row[1])
        else:
            raise KeyError('Key: {} not exists.'.format(item))

    def __delitem__(self, key):
        self._delete(key)

    def __len__(self):
        return self._count()