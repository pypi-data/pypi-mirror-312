import os.path
import unittest
import tempfile
from litedbc import LiteDBC, ColumnInfo, Error, match_schemas, get_columns


INIT_SCRIPT = """
BEGIN TRANSACTION;

-- Create the STORE table
CREATE TABLE store (
    name TEXT PRIMARY KEY,
    model INTEGER NOT NULL);

-- Create the RECORD table
CREATE TABLE record (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    store_name TEXT NOT NULL,
    data BLOB,
    CONSTRAINT fk_record_store_name
        FOREIGN KEY (store_name) REFERENCES store(name));

COMMIT;
"""

INSERT_INTO_STORE = "INSERT INTO store VALUES ('my-store', ?)"
INSERT_INTO_RECORD = "INSERT INTO record (store_name, data) VALUES ('my-store', ?)"

SELECT_FROM_STORE = "SELECT * FROM store"
SELECT_FROM_RECORD = "SELECT * FROM record"

DELETE_RECORDS = "DELETE FROM record WHERE store_name='my-store'"


class TestEmptyDatabase(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")

    def tearDown(self):
        # the Try/Except is needed here because I can only
        # benefit from the constructor's "ignore_cleanup_errors=True"
        # from Python 3.10
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass

    def test_without_init_script(self):
        dbc = LiteDBC(self._filename)
        with self.subTest("Test properties"):
            self.assertIsNotNone(dbc.conn)
            self.assertTrue(dbc.is_new)
        with self.subTest("Test list_tables method"):
            n_tables = dbc.list_tables()
            expected = tuple()
            self.assertEqual(expected, n_tables)

    def test_with_init_script(self):
        dbc = LiteDBC(self._filename, init_script=INIT_SCRIPT)
        with self.subTest("Test properties"):
            self.assertIsNotNone(dbc.conn)
            self.assertTrue(dbc.is_new)
        with self.subTest("Test list_tables method"):
            n_tables = dbc.list_tables()
            expected = ("store", "record")
            self.assertEqual(expected, n_tables)

    def test_with_manual_initialization(self):
        dbc = LiteDBC(self._filename)
        with dbc.cursor() as cur:
            cur.executescript(INIT_SCRIPT)
        with self.subTest("Test properties"):
            self.assertIsNotNone(dbc.conn)
            self.assertTrue(dbc.is_new)
        with self.subTest("Test list_tables method"):
            n_tables = dbc.list_tables()
            expected = ("store", "record")
            self.assertEqual(expected, n_tables)


class TestEmptyInMemoryDatabase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_without_init_script(self):
        dbc = LiteDBC()
        with self.subTest("Test properties"):
            self.assertIsNotNone(dbc.conn)
            self.assertTrue(dbc.is_new)
            self.assertEqual(":memory:", dbc.filename)
        with self.subTest("Test list_tables method"):
            n_tables = dbc.list_tables()
            expected = tuple()
            self.assertEqual(expected, n_tables)

    def test_with_init_script(self):
        dbc = LiteDBC(init_script=INIT_SCRIPT)
        with self.subTest("Test properties"):
            self.assertIsNotNone(dbc.conn)
            self.assertTrue(dbc.is_new)
            self.assertEqual(":memory:", dbc.filename)
        with self.subTest("Test list_tables method"):
            n_tables = dbc.list_tables()
            expected = ("store", "record")
            self.assertEqual(expected, n_tables)

    def test_with_manual_initialization(self):
        dbc = LiteDBC()
        dbc.execute_script(INIT_SCRIPT)
        with self.subTest("Test properties"):
            self.assertIsNotNone(dbc.conn)
            self.assertTrue(dbc.is_new)
            self.assertEqual(":memory:", dbc.filename)
        with self.subTest("Test list_tables method"):
            n_tables = dbc.list_tables()
            expected = ("store", "record")
            self.assertEqual(expected, n_tables)


class TestDatabaseWithData(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        self._dbc = LiteDBC(self._filename, init_script=INIT_SCRIPT)

    def tearDown(self):
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass

    def test(self):
        model, bin_data = 42, b'some bin'
        # insert into store
        with self.subTest():
            n = self._dbc.execute(INSERT_INTO_STORE, (model, ))
            self.assertEqual(1, n)

        # check last_rowid
        with self.subTest():
            self.assertEqual(1, self._dbc.last_rowid)

        # insert into record
        with self.subTest():
            n = self._dbc.execute(INSERT_INTO_RECORD, (bin_data, ))
            self.assertEqual(1, n)

        # check last_rowid
        with self.subTest():
            self.assertEqual(1, self._dbc.last_rowid)

        # select from store
        with self.subTest():
            r = self._dbc.fetch_all(SELECT_FROM_STORE)
            expected = (("my-store", model), )
            self.assertEqual(expected, r)

        # check cached_columns
        with self.subTest():
            self.assertEqual(("name", "model"), self._dbc.last_columns)

        # select from record
        with self.subTest():
            r = list()
            for row in self._dbc.fetch(SELECT_FROM_RECORD):
                r.append(row)
            expected = [(1, 'my-store', bin_data)]
            self.assertEqual(expected, r)

        # check cached columns
        with self.subTest():
            self.assertEqual(("id", "store_name", "data"), self._dbc.last_columns)

        # delete record
        with self.subTest():
            n = self._dbc.execute(DELETE_RECORDS)
            self.assertEqual(1, n)

        # check cached_columns
        with self.subTest():
            self.assertEqual(tuple(), self._dbc.last_columns)

        # select from record
        with self.subTest():
            r = self._dbc.fetch_all(SELECT_FROM_RECORD)
            self.assertEqual(tuple(), r)


class TestTransactionContext(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        self._dbc = LiteDBC(self._filename, init_script=INIT_SCRIPT)

    def tearDown(self):
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass

    def test_simple_transaction(self):
        log = list()
        self._dbc.conn.set_trace_callback(lambda query: log.append(query))
        # create transaction
        with self.subTest():
            with self._dbc.transaction():
                self._dbc.execute(INSERT_INTO_STORE, (42, ))
                r = self._dbc.fetch_all(SELECT_FROM_STORE)
                expected = (("my-store", 42), )
                self.assertEqual(expected, r)
        # check log
        with self.subTest():
            expected = ["BEGIN TRANSACTION",
                        "INSERT INTO store VALUES ('my-store', 42)",
                        "SELECT * FROM store",
                        "COMMIT"]
            self.assertEqual(expected, log)

    def test_nested_transaction(self):
        log = list()
        self._dbc.conn.set_trace_callback(lambda query: log.append(query))
        # create transaction
        with self.subTest():
            with self._dbc.transaction():
                self._dbc.execute(INSERT_INTO_STORE, (42, ))
                with self._dbc.transaction():
                    r = self._dbc.fetch_all(SELECT_FROM_STORE)
                    expected = (("my-store", 42), )
                    self.assertEqual(expected, r)
        # check log
        with self.subTest():
            expected = ["BEGIN TRANSACTION",
                        "INSERT INTO store VALUES ('my-store', 42)",
                        "SELECT * FROM store",
                        "COMMIT"]
            self.assertEqual(expected, log)

    def test_invalid_transactions(self):
        with self.subTest():
            with self.assertRaises(errors.Error):
                with self._dbc.transaction():
                    filename = os.path.join(self._tempdir.name, "export.sql")
                    self._dbc.dump(filename)

        with self.subTest():
            with self.assertRaises(errors.Error):
                with self._dbc.transaction():
                    self._dbc.execute_script("")

        with self.subTest():
            with self.assertRaises(errors.Error):
                with self._dbc.transaction():
                    filename = os.path.join(self._tempdir.name, "backup.db")
                    self._dbc.backup(filename)

        with self.subTest():
            with self.assertRaises(errors.Error):
                with self._dbc.transaction():
                    self._dbc.close()

        with self.subTest():
            with self.assertRaises(errors.Error):
                with self._dbc.transaction():
                    self._dbc.destroy()


class TestBackup(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        self._backup_filename = os.path.join(self._tempdir.name, "backup.db")
        self._dbc = LiteDBC(self._filename, init_script=INIT_SCRIPT)

    def tearDown(self):
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass

    def test(self):
        self._dbc.backup(self._backup_filename)
        new_dbc = LiteDBC(self._backup_filename)
        with self.subTest():
            r = LiteDBC.match(self._dbc, new_dbc)
            self.assertTrue(r)
        with self.subTest():
            n = new_dbc.execute("DROP TABLE record")
            self.assertEqual(-1, n)
            r = LiteDBC.match(self._dbc, new_dbc)
            self.assertFalse(r)


class TestExport(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        self._export_filename = os.path.join(self._tempdir.name, "export.sql")
        self._dbc = LiteDBC(self._filename, init_script=INIT_SCRIPT)

    def tearDown(self):
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass

    def test(self):
        self._dbc.execute(INSERT_INTO_STORE, (42, ))
        r = self._dbc.dump(self._export_filename)
        with open(self._export_filename, "r") as file:
            text = file.read()
        expected = "\n".join(self._dbc.conn.iterdump())
        self.assertEqual(expected, r)
        self.assertEqual(expected, text)


class TestCopyDbc(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        self._dbc = LiteDBC(self._filename, init_script=INIT_SCRIPT)

    def tearDown(self):
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass

    def test(self):
        new_dbc = self._dbc.copy()
        r = LiteDBC.match(self._dbc, new_dbc)
        self.assertTrue(r)


class TestTableInspection(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        self._dbc = LiteDBC(self._filename, init_script=INIT_SCRIPT)

    def tearDown(self):
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass

    def test_existent_store_table(self):
        r = self._dbc.inspect("store")
        expected = (ColumnInfo(cid=0,
                               name='name',
                               type='TEXT',
                               not_null=False,
                               default=None,
                               primary_key=1,
                               foreign_key=None,
                               index_info=(0, 0, 0, True, 'pk')),
                    ColumnInfo(cid=1,
                               name='model',
                               type='INTEGER',
                               not_null=True,
                               default=None,
                               primary_key=0,
                               foreign_key=None,
                               index_info=None))
        self.assertEqual(expected, r)

    def test_existent_record_table(self):
        r = self._dbc.inspect("record")
        expected = (ColumnInfo(cid=0,
                               name='id',
                               type='INTEGER',
                               not_null=False,
                               default=None,
                               primary_key=1,
                               foreign_key=None,
                               index_info=None),
                    ColumnInfo(cid=1,
                               name='store_name',
                               type='TEXT',
                               not_null=True,
                               default=None,
                               primary_key=0,
                               foreign_key=(0, 0, 'store', 'name'),
                               index_info=None),
                    ColumnInfo(cid=2,
                               name='data',
                               type='BLOB',
                               not_null=False,
                               default=None,
                               primary_key=0,
                               foreign_key=None,
                               index_info=None))
        self.assertEqual(expected, r)

    def test_nonexistent_table(self):
        with self.assertRaises(errors.Error):
            self._dbc.inspect("nonexistent-table")


class TestCloseAndDelete(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        self._dbc = LiteDBC(self._filename, init_script=INIT_SCRIPT)

    def tearDown(self):
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass

    def test_close(self):
        with self.subTest():
            self.assertFalse(self._dbc.is_closed)
            self.assertIsNotNone(self._dbc.conn)

        with self.subTest():
            r = self._dbc.close()
            self.assertTrue(r)

        with self.subTest():
            self.assertTrue(self._dbc.is_closed)
            self.assertFalse(self._dbc.is_destroyed)
            self.assertIsNone(self._dbc.conn)

        with self.subTest():
            with self.assertRaises(Exception):
                self._dbc.fetch_all(SELECT_FROM_STORE)

        with self.subTest():
            r = self._dbc.close()
            self.assertFalse(r)
            self.assertTrue(os.path.isfile(self._filename))

        with self.subTest():
            r = self._dbc.destroy()
            self.assertTrue(r)
            self.assertFalse(os.path.isfile(self._filename))

    def test_delete(self):
        with self.subTest():
            self.assertTrue(os.path.isfile(self._filename))

        with self.subTest():
            r = self._dbc.destroy()
            self.assertTrue(r)
            self.assertFalse(os.path.isfile(self._filename))

        with self.subTest():
            self.assertTrue(self._dbc.is_destroyed)
            self.assertTrue(self._dbc.is_closed)
            self.assertIsNone(self._dbc.conn)

        with self.subTest():
            with self.assertRaises(Exception):
                self._dbc.fetch_all(SELECT_FROM_STORE)

        with self.subTest():
            r = self._dbc.close()
            self.assertFalse(r)


if __name__ == "__main__":
    unittest.main()
