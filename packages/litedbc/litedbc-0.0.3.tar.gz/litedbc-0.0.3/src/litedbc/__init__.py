"""Dbc class, useful functions and exception classes"""
import os
import os.path
import sys
import atexit
import threading
import sqlite3 as sqlite
import pathlib
from collections import namedtuple
from litedbc import misc, errors
from litedbc.cursor import Cursor
from litedbc.transaction import Transaction
from litedbc.const import TransactionMode, LockingMode, JournalMode, SyncMode


__all__ = ["LiteDBC", "ColumnInfo", "LockingMode", "JournalMode",
           "SyncMode", "TransactionMode", "Transaction",
           "Cursor", "sqlite"]


CLOSED_DATABASE_MSG = "Cannot operate on a closed database."
ColumnInfo = namedtuple("ColumnInfo", ["cid", "name", "type",
                                       "not_null", "default",
                                       "primary_key", "foreign_key",
                                       "index_info"])


class LiteDBC:
    """
    Database connector
    """
    def __init__(self, filename=None, init_script=None,
                 auto_create=True, is_readonly=False,
                 timeout=5.0, detect_types=0,
                 cached_statements=128,
                 on_create_db=None, on_create_conn=None,
                 row_factory=None, text_factory=None):
        """
        Init

        [parameters]
        - filename: path to SQLite file, either string or a pathlib.Path instance.
            Leave this parameter to None if you want to create an in-memory database
        - init_script: SQL script (string)
        - conn_config: keywords-arguments to pass to sqlite.connect()
        - on_create_db: callback called just after the creation of the database,
            before the execution of init_script and the other on_create_db callback.
            This callback must accept the dbc instance as argument
        - on_create_conn: callback called just after the connection to the database
            and the execution of on_create_db.
            This callback must accept the dbc instance as argument
        """
        self._filename = misc.ensure_db_filename(filename)
        self._init_script = init_script
        self._auto_create = auto_create
        self._is_readonly = misc.get_readonly_value(self._filename, is_readonly)
        self._timeout = timeout
        self._detect_types = detect_types
        self._cached_statements = cached_statements
        self._on_create_db = on_create_db
        self._on_create_conn = on_create_conn
        self._row_factory = row_factory
        self._text_factory = str if text_factory is None else text_factory
        self._write_lock = threading.RLock()
        self._vars_lock = threading.RLock()
        self._in_memory = True if self._filename == ":memory:" else False
        self._is_closed = False
        self._is_destroyed = False
        self._is_new = True if self._in_memory else False
        self._context_count = 0
        self._transaction_context_count = 0
        self._conn = None
        self._setup()

    # ====================================
    #              PROPERTIES
    # ====================================

    @property
    def filename(self):
        return self._filename

    @property
    def init_script(self):
        return self._init_script

    @property
    def auto_create(self):
        return self._auto_create

    @property
    def is_readonly(self):
        return self._is_readonly

    @property
    def timeout(self):
        return self._timeout

    @property
    def detect_types(self):
        return self._detect_types

    @property
    def cached_statements(self):
        return self._cached_statements

    @property
    def on_create_db(self):
        return self._on_create_db

    @property
    def on_create_conn(self):
        return self._on_create_conn

    @property
    def row_factory(self):
        return self._conn.row_factory

    @property
    def text_factory(self):
        return self._conn.text_factory

    @property
    def in_memory(self):
        return self._in_memory

    @property
    def in_transaction(self):
        return self._conn.in_transaction

    @property
    def total_changes(self):
        return self._conn.total_changes

    @property
    def write_lock(self):
        return self._write_lock

    @property
    def is_new(self):
        """
        Returns True if the database has just been created, otherwise returns False
        """
        return self._is_new

    @property
    def is_closed(self):
        """Boolean to tell whether this database is closed or not"""
        with self._vars_lock:
            return self._is_closed

    @property
    def is_destroyed(self):
        """Boolean to tell whether this database has been destroyed via this connection instance or not"""
        with self._vars_lock:
            return self._is_destroyed

    def transaction(self, transaction_mode=TransactionMode.DEFERRED):
        """Returns a context manager"""
        return Transaction(self, self._conn, mode=transaction_mode)

    def deferred_transaction(self):
        """Returns a context manager"""
        return Transaction(self, self._conn, mode=TransactionMode.DEFERRED)

    def immediate_transaction(self):
        """Returns a context manager"""
        return Transaction(self, self._conn, mode=TransactionMode.IMMEDIATE)

    def exclusive_transaction(self):
        """Returns a context manager"""
        return Transaction(self, self._conn, mode=TransactionMode.EXCLUSIVE)

    def cursor(self):
        """Returns a context manager"""
        return Cursor(self, self._conn)

    def execute(self, sql, params=None, /):
        cur = Cursor(self, self._conn)
        return cur.execute(sql, params)

    def executemany(self, sql, params=None, /):
        cur = Cursor(self, self._conn)
        return cur.executemany(sql, params)

    def executescript(self, sql_script, /, transaction_mode=TransactionMode.DEFERRED):
        cur = Cursor(self, self._conn)
        return cur.executescript(sql_script, transaction_mode=transaction_mode)

    def list_tables(self):
        """
        Returns a tuple list of tables names.
        """
        with self.cursor() as cur:
            query = ("SELECT name FROM sqlite_master "
                     "WHERE type='table' AND name NOT LIKE 'sqlite_%'")
            cur.execute(query)
            return tuple([item[0] for item in cur.fetch()])

    def inspect(self, table):
        """
        Returns information about the columns of a given table

        [parameters]
        - table: name of the table to inspect

        [return]
        Returns a tuple containing ColumnInfo instances.
        A ColumnInfo instance is a namedtuple:
            namedtuple(col_id, name, type, not_null, default, primary_key, foreign_key, index_info)
        """
        with self.cursor() as cur:
            result = list()
            foreign_keys = self._get_foreign_keys(table)
            indexes = self._get_indexes(table)
            cur.execute('PRAGMA table_info("{}")'.format(table))
            for row in cur.fetch():
                cid, name, dtype, not_null, default, pk = row
                not_null = bool(not_null)
                fk = foreign_keys.get(name)
                index_info = indexes.get(name)
                info = ColumnInfo(cid, name, dtype, not_null, default, pk, fk, index_info)
                result.append(info)
            if not result:
                raise errors.Error("Non-existent table ({})".format(table))
            return tuple(result)

    def dump(self, dst=None):
        """
        Export the database:

        [parameter]
        - dst_filename: destination filename

        [return]
        it returns a string of sql code if dst isn't set
        """
        with self._write_lock:
            if dst is None:
                return "\n".join(self._conn.iterdump())
            with open(dst, "w", encoding="utf-8") as file:
                for line in self._conn.iterdump():
                    file.write(line + "\n")

    def match(self, target_dbc):
        """Match two database via their connectors.
        All tables defined in alpha_dbc should be in beta_dbc that might have additional tables."""
        for ref_table in self.list_tables():
            alpha_cols = self.inspect(ref_table)
            try:
                beta_cols = target_dbc.inspect(ref_table)
            except errors.Error as e:
                return False
            n = len(alpha_cols)
            if n != len(beta_cols):
                return False
            for i in range(n):
                if alpha_cols[i] != beta_cols[i]:
                    return False
        return True

    def backup(self, dst, *, pages=-1,
               progress=None, name="main",
               sleep=0.250):
        """Create a backup

        [parameters]
        - dst: destination filename"""
        closable_conn = False
        if isinstance(dst, LiteDBC):
            dst_conn = dst.conn
        elif isinstance(dst, sqlite.Connection):
            dst_conn = dst
        else:
            filename = misc.ensure_db_filename(dst)
            dst_conn = sqlite.connect(filename)
            closable_conn = True
        try:
            self._conn.backup(dst_conn, pages=pages,
                              progress=progress, name=name,
                              sleep=sleep)
        finally:
            if closable_conn:
                dst_conn.close()

    def vacuum(self):
        with self.cursor() as cur:
            cur.execute("VACUUM")

    def vacuum_into(self, dst):
        with self.cursor() as cur:
            dst = str(pathlib.Path(dst).resolve())
            cur.execute("VACUUM INTO '{}'".format(dst))

    def copy(self):
        """Creates a new Dbc for the same database file"""
        return self.__copy__()

    def set_locking_mode(self, locking_mode):
        with self.cursor() as cur:
            if isinstance(locking_mode, str):
                locking_mode = locking_mode.upper()
            mode = LockingMode(locking_mode).value
            cur.execute("PRAGMA locking_mode={}".format(mode))
        with self.exclusive_transaction():
            pass

    def get_locking_mode(self):
        with self.cursor() as cur:
            cur.execute("PRAGMA locking_mode")
            locking_mode = cur.fetchone()[0].upper()
            return LockingMode(locking_mode)

    def set_sync_mode(self, sync_mode):
        with self.cursor() as cur:
            if isinstance(sync_mode, str):
                sync_mode = sync_mode.upper()
            mode = SyncMode(sync_mode).value
            cur.execute("PRAGMA synchronous={}".format(mode))

    def get_sync_mode(self):
        with self.cursor() as cur:
            cur.execute("PRAGMA synchronous")
            sync_mode = cur.fetchone()[0].upper()
            return SyncMode(sync_mode)

    def set_journal_mode(self, journal_mode):
        with self.cursor() as cur:
            if isinstance(journal_mode, str):
                journal_mode = journal_mode.upper()
            mode = JournalMode(journal_mode).value
            cur.execute("PRAGMA journal_mode={}".format(mode))
            journal_mode = cur.fetchone()[0].upper()
            return JournalMode(journal_mode)

    def get_journal_mode(self):
        with self.cursor() as cur:
            cur.execute("PRAGMA journal_mode")
            journal_mode = cur.fetchone()[0].upper()
            return JournalMode(journal_mode)

    def blobopen(self, table, column, row, /, *, readonly=False,
                  name ="main"):
        """From Python 3.11"""
        if readonly:
           return self._conn.blob_open(table, column, row,
                                       readonly=readonly, name=name)
        else:
           with self._write_lock:
               return self._conn.blobopen(table, column, row,
                                           readonly=readonly, name=name)

    def create_function(self, name, n_args, func, /, *, deterministic=False):
        return self._conn.create_function(name, n_args, func, deterministic=deterministic)

    def create_aggregate(self, name, n_args, aggregate_cls, /):
        return self._conn.create_aggregate(name, n_args, aggregate_cls)

    def create_window_function(self, name, n_args, aggregate_cls, /):
        return self._conn.create_window_function(name, n_args, aggregate_cls)

    def create_collation(self, name, func, /):
        return self._conn.create_collation(name, func)

    def interrupt(self):
        return self._conn.interrupt()

    def set_authorizer(self, callback):
        return self._conn.set_authorizer(callback)

    def set_progress_handler(self, callback, n):
        return self._conn.set_progress_handler(callback, n)

    def set_trace_callback(self, callback):
        return self._conn.set_trace_callback(callback)

    def enable_load_extension(self, enabled, /):
        return self._conn.enable_load_extension(enabled)

    def load_extension(self, path, /, *, entrypoint=None):
        return self._conn.load_extension(path, entrypoint=entrypoint)

    def iterdump(self):
        return self._conn.iterdump()

    def getlimit(self, category, /):
        return self._conn.getlimit(category)

    def setlimit(self, category, limit, /):
        return self._conn.setlimit(category, limit)

    def getconfig(self, op, /):
        return self._conn.getconfig(op)

    def setconfig(self, op, enable=True, /):
        return self._conn.setconfig(op, enable)

    def serialize(self, *, name="main"):
        return self._conn.serialize(name=name)

    def deserialize(self, data, /, *, name="main"):
        with self._write_lock:
            x = self._conn.deserialize(data, name=name)
            self._in_memory = True
            self._filename = ":memory:"
            return x

    def close(self):
        """
        Closes the connection

        [return]
        Returns a boolean
        """
        with self._write_lock:
            with self._vars_lock:
                is_destroyed, is_closed = self._is_destroyed, self._is_closed
            if is_closed or is_destroyed:
                return False
            try:
                if self._conn is not None:
                    self._conn.close()
            except Exception as e:
                raise
            else:
                with self._vars_lock:
                    self._is_closed = True
            finally:
                atexit.unregister(self.close)
            return True

    def destroy(self):
        """
        Destroy the underlying database file

        [return]
        Returns a boolean
        """
        with self._write_lock:
            with self._vars_lock:
                is_destroyed, is_closed = self._is_destroyed, self._is_closed
            if is_destroyed:
                return False
            if not is_closed:
                self.close()
            if self._in_memory:
                with self._vars_lock:
                    self._is_destroyed = True
                return True
            if os.path.isfile(self._filename):
                os.remove(self._filename)
            else:
                raise errors.Error("Filename not pointing to an actual file.")
            with self._vars_lock:
                self._is_destroyed = True
            return True

    def _setup(self):
        if not self._in_memory:  # therefore, self._filename isn't :memory:
            if ((self._is_readonly or not self._auto_create)
                    and not os.path.isfile(self._filename)):
                raise errors.Error("Missing database.")
            misc.ensure_parent_dir(self._filename)
            if not os.path.isfile(self._filename):
                self._is_new = True
        self._connect()
        if self._is_readonly:
            with self.cursor() as cur:
                cur.execute("PRAGMA query_only=1")

    def _connect(self):
        self._conn = self._create_connection()
        if self._is_new:
            # run the on_create_db if it is provided
            if self._on_create_db is not None:
                self._on_create_db(self)
            # run the initialization script
            if self._init_script:
                with self.transaction() as cur:
                    cur.executescript(self._init_script)
        # run the on_create_conn if it is provided
        if self._on_create_conn is not None:
            self._on_create_conn(self)

    def _create_connection(self):
        # create connection and register with 'atexit' the method to close it
        conn = sqlite.connect(**self._create_conn_config())
        atexit.register(self.close)
        conn.row_factory = self._row_factory
        conn.text_factory = self._text_factory
        return conn

    def _create_conn_config(self):
        # isolation_level is set to None and autocommit is set to True
        # therefore, no transactions are implicitly opened at all.
        # This leaves the underlying SQLite library in autocommit mode
        # allowing the user to perform their own transaction handling
        # using explicit SQL statements.
        conn_config = {"database": self._filename,
                       "timeout": self._timeout,
                       "detect_types": self._detect_types,
                       "isolation_level": None,  # autocommit
                       "check_same_thread": False,
                       "factory": sqlite.Connection,
                       "cached_statements": self._cached_statements,
                       "uri": True if self._filename.startswith("file:") else False}
        if sys.version_info >= (3, 12):
            # For Python 3.12 and later, set autocommit to True
            conn_config["autocommit"] = True
        return conn_config

    def _get_foreign_keys(self, table):
        # this function assumes that 'table' really exists !
        result = dict()
        with self.cursor() as cur:
            cur.execute('PRAGMA foreign_key_list("{}")'.format(table))
            for row in cur.fetch():
                fid, rank, foreign_table, local_name, foreign_name, _, _, _ = row
                result[local_name] = (fid, rank, foreign_table, foreign_name)
        return result

    def _get_indexes(self, table):
        # this function assumes that 'table' really exists !
        result = dict()
        with self.cursor() as cur:
            cur.execute('PRAGMA index_list("{}")'.format(table))
            for row_a in cur.fetch():
                rank1, name, unique, spec, _ = row_a
                cur.execute('PRAGMA index_info("{}")'.format(name))
                for row_b in cur.fetch():
                    rank2, rank3, colname = row_b
                    if colname:
                        result[colname] = (rank1, rank2, rank3, bool(unique), spec)
        return result

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __copy__(self):
        return LiteDBC(self._filename,
                       init_script=self._init_script,
                       is_readonly=self._is_readonly,
                       timeout=self._timeout,
                       detect_types=self._detect_types,
                       cached_statements=self._cached_statements,
                       on_create_db=self._on_create_db,
                       on_create_conn=self._on_create_conn,
                       row_factory=self._row_factory,
                       text_factory=self._text_factory)

    def __del__(self):
        self.close()
