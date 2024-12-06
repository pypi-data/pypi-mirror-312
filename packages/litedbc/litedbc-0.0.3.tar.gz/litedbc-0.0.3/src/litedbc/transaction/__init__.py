from litedbc import misc
from litedbc.cursor import Cursor


class Transaction:
    def __init__(self, dbc, conn, mode):
        self._dbc = dbc
        self._conn = conn
        self._cur = None
        self._mode = mode
        self._is_nested = False

    @property
    def dbc(self):
        return self._dbc

    @property
    def mode(self):
        return self._mode

    @property
    def cursor(self):
        return self._cur

    def __enter__(self):
        self._dbc.write_lock.acquire()
        self._is_nested = True if self._conn.in_transaction else False
        self._cur = Cursor(self._dbc, self._conn)
        if not self._is_nested and self._mode is not None:
            start_transaction_stmt = misc.get_start_transaction_stmt(self._mode)
            self._cur.execute(start_transaction_stmt)
        return self._cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if not self._is_nested and self._conn.in_transaction:
                with self._dbc.write_lock:
                    if exc_type is None:
                        self._conn.execute("COMMIT")
                    else:
                        self._conn.execute("ROLLBACK")
        finally:
            try:
                self._cur.close()
            finally:
                self._dbc.write_lock.release()

    def __del__(self):
        self._cur.close()
