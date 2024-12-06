from litedbc.const import TransactionMode
from litedbc import misc


class Cursor:
    """When the cursor context is not nested, i.e., not created within a transaction,
    it will `ROLLBACK` a pending transaction when you close it (the cursor)"""
    def __init__(self, dbc, conn):
        self._dbc = dbc
        self._conn = conn
        self._write_lock = dbc.write_lock
        self._sqlite_cursor = self._conn.cursor()
        self._is_nested = self._conn.in_transaction

    @property
    def dbc(self):
        return self._dbc

    @property
    def arraysize(self):
        return self._sqlite_cursor.arraysize

    @arraysize.setter
    def arraysize(self, val):
        self._sqlite_cursor.arraysize = val

    @property
    def description(self):
        return self._sqlite_cursor.description

    @property
    def lastrowid(self):
        return self._sqlite_cursor.lastrowid

    @property
    def rowcount(self):
        return self._sqlite_cursor.rowcount

    @property
    def row_factory(self):
        return self._sqlite_cursor.row_factory

    @row_factory.setter
    def row_factory(self, val):
        self._sqlite_cursor.row_factory = val

    def execute(self, sql, params=None, /):
        sql = sql.strip()
        params = tuple() if params is None else params
        if misc.is_stmt("SELECT", sql):
            self._sqlite_cursor.execute(sql, params)
            return self
        with self._write_lock:
            self._sqlite_cursor.execute(sql, params)
            return self

    def executemany(self, sql, params=None, /):
        sql = sql.strip()
        params = tuple() if params is None else params
        with self._write_lock:
            self._sqlite_cursor.executemany(sql, params)
            return self

    def executescript(self, sql_script, /, transaction_mode=TransactionMode.DEFERRED):
        with self._write_lock:
            sql_script = sql_script.strip()
            in_transaction = self._conn.in_transaction
            transactional = False if transaction_mode is None else True
            if transactional and not in_transaction:
                start_transaction_stmt = misc.get_start_transaction_stmt(transaction_mode)
                self._sqlite_cursor.execute(start_transaction_stmt)
            self._sqlite_cursor.executescript(sql_script)
            if transactional and not in_transaction:
                self._sqlite_cursor.execute("COMMIT")
            return self

    def fetch(self, limit=None, buffer_size=None):
        limit = -1 if limit is None else limit
        buffer_size = self._sqlite_cursor.arraysize if buffer_size is None else buffer_size
        rows = self._sqlite_cursor.fetchmany(buffer_size)
        i = 0
        while rows:
            for r in rows:
                if limit == i:
                    return
                yield r
                i += 1
            rows = self._sqlite_cursor.fetchmany(buffer_size)

    def fetchone(self):
        return self._sqlite_cursor.fetchone()

    def fetchmany(self, size=None):
        size = self._sqlite_cursor.arraysize if size is None else size
        return self._sqlite_cursor.fetchmany(size)

    def fetchall(self):
        return self._sqlite_cursor.fetchall()

    def get_columns(self):
        columns = tuple()
        if self._sqlite_cursor.description:
            columns = tuple([d[0] for d in self._sqlite_cursor.description])
        return columns

    def setinputsizes(self, sizes, /):
        """Required by the DB-API. Does nothing in sqlite3."""
        pass

    def setoutputsize(size, column=None, /):
        """Required by the DB-API. Does nothing in sqlite3."""
        pass

    def close(self):
        with self._write_lock:
            if not self._is_nested and self._conn.in_transaction:
                self._sqlite_cursor.execute("ROLLBACK")
            return self._sqlite_cursor.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __iter__(self):
        return self

    def __next__(self):
        r = self._sqlite_cursor.fetchone()
        if r is None:
            raise StopIteration
        return r
