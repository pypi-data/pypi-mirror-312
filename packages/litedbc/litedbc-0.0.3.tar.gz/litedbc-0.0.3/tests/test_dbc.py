import os.path
import unittest
import tempfile
from litedbc import LiteDBC, LockingMode, ColumnInfo
from litedbc.errors import Error, OperationalError, ProgrammingError


INIT_SCRIPT = """
-- Create the GALAXY table
CREATE TABLE galaxy (
    name TEXT PRIMARY KEY,
    size INTEGER NOT NULL);

-- Create the PLANET table
CREATE TABLE planet (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    signature BLOB,
    galaxy_name TEXT NOT NULL,
    CONSTRAINT fk_planet_galaxy_name
        FOREIGN KEY (galaxy_name) REFERENCES galaxy(name));
"""

INSERT_INTO_GALAXY = "INSERT INTO galaxy VALUES (?, ?)"
INSERT_INTO_PLANET = "INSERT INTO planet (galaxy_name, signature) VALUES (?, ?)"

SELECT_FROM_GALAXY = "SELECT * FROM galaxy"
SELECT_FROM_PLANET = "SELECT * FROM planet"

DELETE_PLANETS = "DELETE FROM planet WHERE galaxy_name=?"

GALAXY_NAME = "aldebaran"
GALAXY_SIZE = 42
PLANET_SIGNATURE = b'planet-signature'


def populate_db(dbc):
    with dbc.transaction() as cur:
        # insert into galaxy
        cur.execute(INSERT_INTO_GALAXY, (GALAXY_NAME, GALAXY_SIZE))
        # insert into planet
        cur.execute(INSERT_INTO_PLANET, (GALAXY_NAME, PLANET_SIGNATURE))


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
        with LiteDBC(self._filename) as dbc:
            with self.subTest("Test properties"):
                self.assertTrue(dbc.is_new)
            with self.subTest("Test list_tables method"):
                n_tables = dbc.list_tables()
                expected = tuple()
                self.assertEqual(expected, n_tables)

    def test_with_init_script(self):
        with LiteDBC(self._filename, init_script=INIT_SCRIPT) as dbc:
            with self.subTest("Test properties"):
                self.assertTrue(dbc.is_new)
            with self.subTest("Test list_tables method"):
                n_tables = dbc.list_tables()
                expected = ("galaxy", "planet")
                self.assertEqual(expected, n_tables)

    def test_with_manual_initialization(self):
        with LiteDBC(self._filename) as dbc:
            with dbc.cursor() as cur:
                cur.executescript(INIT_SCRIPT)
            with self.subTest("Test properties"):
                self.assertTrue(dbc.is_new)
            with self.subTest("Test list_tables method"):
                n_tables = dbc.list_tables()
                expected = ("galaxy", "planet")
                self.assertEqual(expected, n_tables)

    def test_auto_create_off(self):
        with self.assertRaises(Error):
            with LiteDBC(self._filename, auto_create=False) as dbc:
                pass



class TestEmptyInMemoryDatabase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_without_init_script(self):
        dbc = LiteDBC()
        with self.subTest("Test properties"):
            self.assertTrue(dbc.is_new)
            self.assertEqual(":memory:", dbc.filename)
        with self.subTest("Test list_tables method"):
            n_tables = dbc.list_tables()
            expected = tuple()
            self.assertEqual(expected, n_tables)

    def test_with_init_script(self):
        dbc = LiteDBC(init_script=INIT_SCRIPT)
        with self.subTest("Test properties"):
            self.assertTrue(dbc.is_new)
            self.assertEqual(":memory:", dbc.filename)
        with self.subTest("Test list_tables method"):
            n_tables = dbc.list_tables()
            expected = ("galaxy", "planet")
            self.assertEqual(expected, n_tables)

    def test_with_manual_initialization(self):
        dbc = LiteDBC()
        with dbc.cursor() as cur:
            cur.executescript(INIT_SCRIPT)
        with self.subTest("Test properties"):
            self.assertTrue(dbc.is_new)
            self.assertEqual(":memory:", dbc.filename)
        with self.subTest("Test list_tables method"):
            n_tables = dbc.list_tables()
            expected = ("galaxy", "planet")
            self.assertEqual(expected, n_tables)


class TestDatabaseWithData(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        self._dbc = LiteDBC(self._filename, init_script=INIT_SCRIPT)

    def tearDown(self):
        # the Try/Except is needed here because I can only
        # benefit from the constructor's "ignore_cleanup_errors=True"
        # from Python 3.10
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass
        self._dbc.close()

    def test(self):
        # insert into galaxy
        with self.subTest():
            with self._dbc.cursor() as cur:
                cur.execute(INSERT_INTO_GALAXY, (GALAXY_NAME, GALAXY_SIZE))
                self.assertEqual(1, cur.lastrowid)
        # insert into planet
        with self.subTest():
            with self._dbc.cursor() as cur:
                cur.execute(INSERT_INTO_PLANET, (GALAXY_NAME, PLANET_SIGNATURE))
                self.assertEqual(1, cur.lastrowid)
        # select from galaxy
        with self.subTest():
            with self._dbc.cursor() as cur:
                cur.execute(SELECT_FROM_GALAXY)
                r = cur.fetchall()
                expected = ((GALAXY_NAME, GALAXY_SIZE), )
                self.assertEqual(expected, tuple(r))
        # delete planet
        with self.subTest():
            with self._dbc.cursor() as cur:
                cur.execute(DELETE_PLANETS, (GALAXY_NAME, ))
                self.assertEqual(1, cur.lastrowid)
        # select from planet
        with self.subTest():
            with self._dbc.cursor() as cur:
                cur.execute(SELECT_FROM_PLANET)
                r = cur.fetchall()
                self.assertEqual(tuple(), tuple(r))


class TestDirectExecution(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        self._dbc = LiteDBC(self._filename, init_script=INIT_SCRIPT)

    def tearDown(self):
        # the Try/Except is needed here because I can only
        # benefit from the constructor's "ignore_cleanup_errors=True"
        # from Python 3.10
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass
        self._dbc.close()

    def test(self):
        # insert into galaxy
        with self.subTest():
            cur = self._dbc.execute(INSERT_INTO_GALAXY, (GALAXY_NAME, GALAXY_SIZE))
            self.assertEqual(1, cur.lastrowid)
        # insert into planet
        with self.subTest():
            cur = self._dbc.execute(INSERT_INTO_PLANET, (GALAXY_NAME, PLANET_SIGNATURE))
            self.assertEqual(1, cur.lastrowid)
        # select from galaxy
        with self.subTest():
            cur = self._dbc.execute(SELECT_FROM_GALAXY)
            r = cur.fetchall()
            expected = ((GALAXY_NAME, GALAXY_SIZE), )
            self.assertEqual(expected, tuple(r))
        # delete planet
        with self.subTest():
            cur = self._dbc.execute(DELETE_PLANETS, (GALAXY_NAME, ))
            self.assertEqual(1, cur.lastrowid)
        # select from planet
        with self.subTest():
            cur = self._dbc.execute(SELECT_FROM_PLANET)
            r = cur.fetchall()
            self.assertEqual(tuple(), tuple(r))


class TestExecuteScript(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        self._dbc = LiteDBC(self._filename)
        self._script = """
        CREATE TABLE galaxy (name TEXT PRIMARY KEY, size INTEGER NOT NULL);
        """

    def tearDown(self):
        # the Try/Except is needed here because I can only
        # benefit from the constructor's "ignore_cleanup_errors=True"
        # from Python 3.10
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass
        self._dbc.close()

    def test_executescript_within_transaction_context(self):
        log = list()
        self._dbc.set_trace_callback(lambda query: log.append(query))
        with self._dbc.immediate_transaction() as cursor:
            cursor.executescript(self._script)
        expected = ['BEGIN IMMEDIATE',
                    'CREATE TABLE galaxy (name TEXT PRIMARY KEY, size INTEGER NOT NULL);',
                    'COMMIT']
        self.assertEqual(expected, log)

    def test_executescript_within_cursor_context(self):
        log = list()
        self._dbc.set_trace_callback(lambda query: log.append(query))
        with self._dbc.cursor() as cur:
            cur.executescript(self._script)
        expected = ['BEGIN DEFERRED',
                    'CREATE TABLE galaxy (name TEXT PRIMARY KEY, size INTEGER NOT NULL);',
                    'COMMIT']
        self.assertEqual(expected, log)

    def test_executescript_outside_context(self):
        log = list()
        self._dbc.set_trace_callback(lambda query: log.append(query))
        self._dbc.executescript(self._script)
        expected = ['BEGIN DEFERRED',
                    'CREATE TABLE galaxy (name TEXT PRIMARY KEY, size INTEGER NOT NULL);',
                    'COMMIT']
        self.assertEqual(expected, log)




class TestDbcWithContextManager(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")

    def tearDown(self):
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass

    def test(self):
        with LiteDBC(self._filename, init_script=INIT_SCRIPT) as dbc:
            with self.subTest():
                self.assertFalse(dbc.is_closed)
        with self.subTest():
            self.assertTrue(dbc.is_closed)


class TestCursorContext(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        self._dbc = LiteDBC(self._filename, init_script=INIT_SCRIPT)

    def tearDown(self):
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass
        self._dbc.close()

    def test_context(self):
        log = list()
        self._dbc.set_trace_callback(lambda query: log.append(query))
        # create transaction
        with self.subTest():
            with self._dbc.cursor() as cur:
                cur.execute(INSERT_INTO_GALAXY, (GALAXY_NAME, GALAXY_SIZE))
                cur.execute(SELECT_FROM_GALAXY)
                r = cur.fetchall()
                expected = ((GALAXY_NAME, GALAXY_SIZE), )
                self.assertEqual(expected, tuple(r))
        # check log
        with self.subTest():
            expected = ["INSERT INTO galaxy VALUES ('{}', {})".format(GALAXY_NAME,
                                                                      GALAXY_SIZE),
                        "SELECT * FROM galaxy"]
            self.assertEqual(expected, log)

    def test_nested_context(self):
        log = list()
        self._dbc.set_trace_callback(lambda query: log.append(query))
        # create transaction
        with self.subTest():
            with self._dbc.cursor() as cur:
                cur.execute(INSERT_INTO_GALAXY, (GALAXY_NAME, GALAXY_SIZE))
                with self._dbc.cursor() as cur:
                    cur.execute(SELECT_FROM_GALAXY)
                    r = cur.fetchall()
                    expected = ((GALAXY_NAME, GALAXY_SIZE), )
                    self.assertEqual(expected, tuple(r))
        # check log
        with self.subTest():
            expected = ["INSERT INTO galaxy VALUES ('{}', {})".format(GALAXY_NAME,
                                                                      GALAXY_SIZE),
                        "SELECT * FROM galaxy"]
            self.assertEqual(expected, log)

    def test_context_with_uncommitted_transaction(self):
        log = list()
        self._dbc.set_trace_callback(lambda query: log.append(query))
        # create transaction
        with self.subTest():
            with self._dbc.cursor() as cur:
                cur.execute("BEGIN DEFERRED")
                cur.execute(INSERT_INTO_GALAXY, (GALAXY_NAME, GALAXY_SIZE))
                cur.execute(SELECT_FROM_GALAXY)
                r = cur.fetchall()
                expected = ((GALAXY_NAME, GALAXY_SIZE),)
                self.assertEqual(expected, tuple(r))
        # check log
        with self.subTest():
            expected = ["BEGIN DEFERRED",
                        "INSERT INTO galaxy VALUES ('{}', {})".format(GALAXY_NAME,
                                                                      GALAXY_SIZE),
                        "SELECT * FROM galaxy",
                        "ROLLBACK"]
            self.assertEqual(expected, log)

    def test_context_with_rollback(self):
        log = list()
        self._dbc.set_trace_callback(lambda query: log.append(query))
        # create transaction
        with self.subTest():
            with self.assertRaises(Exception):
                with self._dbc.cursor() as cur:
                    cur.execute("BEGIN DEFERRED")
                    cur.execute(INSERT_INTO_GALAXY, (GALAXY_NAME, GALAXY_SIZE))
                    raise Exception

        # check log
        with self.subTest():
            expected = ["BEGIN DEFERRED",
                        "INSERT INTO galaxy VALUES ('{}', {})".format(GALAXY_NAME,
                                                                      GALAXY_SIZE),
                        "ROLLBACK"]
            self.assertEqual(expected, log)


class TestCursorAsIterator(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        self._dbc = LiteDBC(self._filename, init_script=INIT_SCRIPT)

    def tearDown(self):
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass
        self._dbc.close()

    def test(self):
        with self.subTest():
            with self._dbc.cursor() as cur:
                cur.execute(INSERT_INTO_GALAXY, (GALAXY_NAME, GALAXY_SIZE))
                r = tuple(cur.execute(SELECT_FROM_GALAXY))
                expected = ((GALAXY_NAME, GALAXY_SIZE), )
                self.assertEqual(expected, tuple(r))
                self.assertEqual(tuple(), tuple(cur))


class TestDeferredTransactionContext(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        self._dbc = LiteDBC(self._filename, init_script=INIT_SCRIPT)

    def tearDown(self):
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass
        self._dbc.close()

    def test_context(self):
        log = list()
        self._dbc.set_trace_callback(lambda query: log.append(query))
        # create transaction
        with self.subTest():
            with self._dbc.transaction() as cur:
                cur.execute(INSERT_INTO_GALAXY, (GALAXY_NAME, GALAXY_SIZE))
                cur.execute(SELECT_FROM_GALAXY)
                r = cur.fetchall()
                expected = ((GALAXY_NAME, GALAXY_SIZE), )
                self.assertEqual(expected, tuple(r))
        # check log
        with self.subTest():
            expected = ["BEGIN DEFERRED",
                        "INSERT INTO galaxy VALUES ('{}', {})".format(GALAXY_NAME,
                                                                      GALAXY_SIZE),
                        "SELECT * FROM galaxy",
                        "COMMIT"]
            self.assertEqual(expected, log)

    def test_nested_context(self):
        log = list()
        self._dbc.set_trace_callback(lambda query: log.append(query))
        # create transaction
        with self.subTest():
            with self._dbc.transaction() as cur:
                cur.execute(INSERT_INTO_GALAXY, (GALAXY_NAME, GALAXY_SIZE))
                with self._dbc.transaction() as cur:
                    cur.execute(SELECT_FROM_GALAXY)
                    r = cur.fetchall()
                    expected = ((GALAXY_NAME, GALAXY_SIZE), )
                    self.assertEqual(expected, tuple(r))
        # check log
        with self.subTest():
            expected = ["BEGIN DEFERRED",
                        "INSERT INTO galaxy VALUES ('{}', {})".format(GALAXY_NAME,
                                                                      GALAXY_SIZE),
                        "SELECT * FROM galaxy",
                        "COMMIT"]
            self.assertEqual(expected, log)

    def test_context_with_rollback(self):
        log = list()
        self._dbc.set_trace_callback(lambda query: log.append(query))
        # create transaction
        with self.subTest():
            with self.assertRaises(Exception):
                with self._dbc.transaction() as cur:
                    cur.execute(INSERT_INTO_GALAXY, (GALAXY_NAME, GALAXY_SIZE))
                    raise Exception

        # check log
        with self.subTest():
            expected = ["BEGIN DEFERRED",
                        "INSERT INTO galaxy VALUES ('{}', {})".format(GALAXY_NAME,
                                                                      GALAXY_SIZE),
                        "ROLLBACK"]
            self.assertEqual(expected, log)


class TestImmediateTransactionContext(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        self._dbc = LiteDBC(self._filename, init_script=INIT_SCRIPT)

    def tearDown(self):
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass
        self._dbc.close()

    def test_context(self):
        log = list()
        self._dbc.set_trace_callback(lambda query: log.append(query))
        # create transaction
        with self.subTest():
            with self._dbc.immediate_transaction() as cur:
                cur.execute(INSERT_INTO_GALAXY, (GALAXY_NAME, GALAXY_SIZE))
                cur.execute(SELECT_FROM_GALAXY)
                r = cur.fetchall()
                expected = ((GALAXY_NAME, GALAXY_SIZE), )
                self.assertEqual(expected, tuple(r))
        # check log
        with self.subTest():
            expected = ["BEGIN IMMEDIATE",
                        "INSERT INTO galaxy VALUES ('{}', {})".format(GALAXY_NAME,
                                                                      GALAXY_SIZE),
                        "SELECT * FROM galaxy",
                        "COMMIT"]
            self.assertEqual(expected, log)

    def test_nested_context(self):
        log = list()
        self._dbc.set_trace_callback(lambda query: log.append(query))
        # create transaction
        with self.subTest():
            with self._dbc.immediate_transaction() as cur:
                cur.execute(INSERT_INTO_GALAXY, (GALAXY_NAME, GALAXY_SIZE))
                with self._dbc.immediate_transaction() as cur:
                    cur.execute(SELECT_FROM_GALAXY)
                    r = cur.fetchall()
                    expected = ((GALAXY_NAME, GALAXY_SIZE), )
                    self.assertEqual(expected, tuple(r))
        # check log
        with self.subTest():
            expected = ["BEGIN IMMEDIATE",
                        "INSERT INTO galaxy VALUES ('{}', {})".format(GALAXY_NAME,
                                                                      GALAXY_SIZE),
                        "SELECT * FROM galaxy",
                        "COMMIT"]
            self.assertEqual(expected, log)

    def test_context_with_rollback(self):
        log = list()
        self._dbc.set_trace_callback(lambda query: log.append(query))
        # create transaction
        with self.subTest():
            with self.assertRaises(Exception):
                with self._dbc.immediate_transaction() as cur:
                    cur.execute(INSERT_INTO_GALAXY, (GALAXY_NAME, GALAXY_SIZE))
                    raise Exception

        # check log
        with self.subTest():
            expected = ["BEGIN IMMEDIATE",
                        "INSERT INTO galaxy VALUES ('{}', {})".format(GALAXY_NAME,
                                                                      GALAXY_SIZE),
                        "ROLLBACK"]
            self.assertEqual(expected, log)


class TestExclusiveTransactionContext(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        self._dbc = LiteDBC(self._filename, init_script=INIT_SCRIPT)

    def tearDown(self):
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass
        self._dbc.close()

    def test_context(self):
        log = list()
        self._dbc.set_trace_callback(lambda query: log.append(query))
        # create transaction
        with self.subTest():
            with self._dbc.exclusive_transaction() as cur:
                cur.execute(INSERT_INTO_GALAXY, (GALAXY_NAME, GALAXY_SIZE))
                cur.execute(SELECT_FROM_GALAXY)
                r = cur.fetchall()
                expected = ((GALAXY_NAME, GALAXY_SIZE), )
                self.assertEqual(expected, tuple(r))
        # check log
        with self.subTest():
            expected = ["BEGIN EXCLUSIVE",
                        "INSERT INTO galaxy VALUES ('{}', {})".format(GALAXY_NAME,
                                                                      GALAXY_SIZE),
                        "SELECT * FROM galaxy",
                        "COMMIT"]
            self.assertEqual(expected, log)

    def test_nested_context(self):
        log = list()
        self._dbc.set_trace_callback(lambda query: log.append(query))
        # create transaction
        with self.subTest():
            with self._dbc.exclusive_transaction() as cur:
                cur.execute(INSERT_INTO_GALAXY, (GALAXY_NAME, GALAXY_SIZE))
                with self._dbc.exclusive_transaction() as cur:
                    cur.execute(SELECT_FROM_GALAXY)
                    r = cur.fetchall()
                    expected = ((GALAXY_NAME, GALAXY_SIZE), )
                    self.assertEqual(expected, tuple(r))
        # check log
        with self.subTest():
            expected = ["BEGIN EXCLUSIVE",
                        "INSERT INTO galaxy VALUES ('{}', {})".format(GALAXY_NAME,
                                                                      GALAXY_SIZE),
                        "SELECT * FROM galaxy",
                        "COMMIT"]
            self.assertEqual(expected, log)

    def test_context_with_rollback(self):
        log = list()
        self._dbc.set_trace_callback(lambda query: log.append(query))
        # create transaction
        with self.subTest():
            with self.assertRaises(Exception):
                with self._dbc.exclusive_transaction() as cur:
                    cur.execute(INSERT_INTO_GALAXY, (GALAXY_NAME, GALAXY_SIZE))
                    raise Exception

        # check log
        with self.subTest():
            expected = ["BEGIN EXCLUSIVE",
                        "INSERT INTO galaxy VALUES ('{}', {})".format(GALAXY_NAME,
                                                                      GALAXY_SIZE),
                        "ROLLBACK"]
            self.assertEqual(expected, log)


class TestMatchFunction(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        self._dbc = LiteDBC(self._filename, init_script=INIT_SCRIPT)

    def tearDown(self):
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass
        self._dbc.close()

    def test(self):
        new_dbc = LiteDBC(self._dbc.filename, init_script=INIT_SCRIPT)
        r = self._dbc.match(new_dbc)
        self.assertTrue(r)


class TestGetColumnsFunction(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        self._dbc = LiteDBC(self._filename, init_script=INIT_SCRIPT)

    def tearDown(self):
        # the Try/Except is needed here because I can only
        # benefit from the constructor's "ignore_cleanup_errors=True"
        # from Python 3.10
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass
        self._dbc.close()

    def test(self):
        populate_db(self._dbc)
        # select from galaxy
        with self.subTest():
            with self._dbc.cursor() as cur:
                cur.execute(SELECT_FROM_GALAXY)
                r = cur.get_columns()
                expected = ("name", "size")
                self.assertEqual(expected, r)
        # select from planet
        with self.subTest():
            with self._dbc.cursor() as cur:
                cur.execute(SELECT_FROM_PLANET)
                r = cur.get_columns()
                expected = ("id", "signature", "galaxy_name")
                self.assertEqual(expected, r)


class TestFetchFunction(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        self._dbc = LiteDBC(self._filename, init_script=INIT_SCRIPT)

    def tearDown(self):
        # the Try/Except is needed here because I can only
        # benefit from the constructor's "ignore_cleanup_errors=True"
        # from Python 3.10
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass
        self._dbc.close()

    def test(self):
        populate_db(self._dbc)
        # select from galaxy
        with self.subTest():
            with self._dbc.cursor() as cur:
                cur.execute(SELECT_FROM_GALAXY)
                r = tuple(cur.fetch())  # 'fetch' is a generator
                expected = ((GALAXY_NAME, GALAXY_SIZE), )
                self.assertEqual(expected, r)
        # select from planet
        with self.subTest():
            with self._dbc.cursor() as cur:
                cur.execute(SELECT_FROM_PLANET)
                r = tuple(cur.fetch())  # 'fetch' is a generator
                expected = ((1, PLANET_SIGNATURE, GALAXY_NAME), )
                self.assertEqual(expected, r)


class TestBackupMethod(unittest.TestCase):

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
        self._dbc.close()

    def test(self):
        self._dbc.backup(self._backup_filename)
        new_dbc = LiteDBC(self._backup_filename)
        with self.subTest():
            r = self._dbc.match(new_dbc)
            self.assertTrue(r)
        with self.subTest():
            with new_dbc.transaction() as cur:
                cur.execute("DROP TABLE planet")
                self.assertEqual(-1, cur.rowcount)
                r = self._dbc.match(new_dbc)
                self.assertFalse(r)


class TestDumpMethod(unittest.TestCase):

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
        self._dbc.close()

    def test_dump_to_file(self):
        with self._dbc.transaction() as cur:
            cur.execute(INSERT_INTO_GALAXY, (GALAXY_NAME, GALAXY_SIZE))
        self._dbc.dump(self._export_filename)
        with open(self._export_filename, "r", encoding="utf-8") as file:
            text = file.read()
        expected = "\n".join(self._dbc.iterdump()) + "\n"
        self.assertEqual(expected, text)

    def test_dump(self):
        with self._dbc.transaction() as cur:
            cur.execute(INSERT_INTO_GALAXY, (GALAXY_NAME, GALAXY_SIZE))
        r = self._dbc.dump()
        expected = "\n".join(self._dbc.iterdump())
        self.assertEqual(expected, r)


class TestCopyDbcMethod(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        self._dbc = LiteDBC(self._filename, init_script=INIT_SCRIPT)

    def tearDown(self):
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass
        self._dbc.close()

    def test(self):
        new_dbc = self._dbc.copy()
        r = self._dbc.match(new_dbc)
        self.assertTrue(r)


class TestTableInspectionMethod(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        self._dbc = LiteDBC(self._filename, init_script=INIT_SCRIPT)

    def tearDown(self):
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass
        self._dbc.close()

    def test_existent_galaxy_table(self):
        r = self._dbc.inspect("galaxy")
        expected = (ColumnInfo(cid=0,
                               name='name',
                               type='TEXT',
                               not_null=False,
                               default=None,
                               primary_key=1,
                               foreign_key=None,
                               index_info=(0, 0, 0, True, 'pk')),
                    ColumnInfo(cid=1,
                               name='size',
                               type='INTEGER',
                               not_null=True,
                               default=None,
                               primary_key=0,
                               foreign_key=None,
                               index_info=None))
        self.assertEqual(expected, r)

    def test_existent_planet_table(self):
        r = self._dbc.inspect("planet")
        expected = (ColumnInfo(cid=0,
                               name='id',
                               type='INTEGER',
                               not_null=False,
                               default=None,
                               primary_key=1,
                               foreign_key=None,
                               index_info=None),
                    ColumnInfo(cid=1,
                               name='signature',
                               type='BLOB',
                               not_null=False,
                               default=None,
                               primary_key=0,
                               foreign_key=None,
                               index_info=None),
                    ColumnInfo(cid=2,
                               name='galaxy_name',
                               type='TEXT',
                               not_null=True,
                               default=None,
                               primary_key=0,
                               foreign_key=(0, 0, 'galaxy', 'name'),
                               index_info=None))
        self.assertEqual(expected, r)

    def test_nonexistent_table(self):
        with self.assertRaises(Error):
            self._dbc.inspect("nonexistent-table")


class TestCloseAndDeleteMethods(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        self._dbc = LiteDBC(self._filename, init_script=INIT_SCRIPT)

    def tearDown(self):
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass
        self._dbc.close()

    def test_close(self):
        with self.subTest():
            self.assertFalse(self._dbc.is_closed)

        with self.subTest():
            r = self._dbc.close()
            self.assertTrue(r)

        with self.subTest():
            self.assertTrue(self._dbc.is_closed)
            self.assertFalse(self._dbc.is_destroyed)

        with self.subTest():
            with self.assertRaises(ProgrammingError):
                with self._dbc.cursor() as cur:
                    cur.fetchall(SELECT_FROM_GALAXY)

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

        with self.subTest():
            with self.assertRaises(ProgrammingError):
                with self._dbc.cursor() as cur:
                    cur.fetchall(SELECT_FROM_GALAXY)

        with self.subTest():
            r = self._dbc.close()
            self.assertFalse(r)


class TestDatabaseLockingMode(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self._filename = os.path.join(self._tempdir.name, "my.db")
        self._dbc = LiteDBC(self._filename, init_script=INIT_SCRIPT,
                            timeout=0)

    def tearDown(self):
        # the Try/Except is needed here because I can only
        # benefit from the constructor's "ignore_cleanup_errors=True"
        # from Python 3.10
        try:
            self._tempdir.cleanup()
        except Exception as e:
            pass
        self._dbc.close()

    def test_normal_locking_mode(self):
        populate_db(self._dbc)
        with self.subTest():
            r = self._dbc.get_locking_mode()
            expected = LockingMode.NORMAL
            self.assertEqual(expected, r)
        # select from galaxy
        with self.subTest():
            with self._dbc.cursor() as cur:
                cur.execute(SELECT_FROM_GALAXY)
                r = tuple(cur.fetch())  # 'fetch' is a generator
                expected = ((GALAXY_NAME, GALAXY_SIZE),)
                self.assertEqual(expected, r)
        # select from galaxy (from another connection)
        with self.subTest():
            new_dbc = self._dbc.copy()
            with new_dbc.cursor() as cur:
                cur.execute(SELECT_FROM_GALAXY)
                r = tuple(cur.fetch())  # 'fetch' is a generator
                expected = ((GALAXY_NAME, GALAXY_SIZE),)
                self.assertEqual(expected, r)

    def test_exclusive_locking_mode(self):
        populate_db(self._dbc)
        with self.subTest():
            self._dbc.set_locking_mode(LockingMode.EXCLUSIVE)
        with self.subTest():
            r = self._dbc.get_locking_mode()
            expected = LockingMode.EXCLUSIVE
            self.assertEqual(expected, r)
        # select from galaxy
        with self.subTest():
            with self._dbc.cursor() as cur:
                cur.execute(SELECT_FROM_GALAXY)
                r = tuple(cur.fetch())  # 'fetch' is a generator
                expected = ((GALAXY_NAME, GALAXY_SIZE),)
                self.assertEqual(expected, r)
        # select from galaxy (from another connection)
        with self.subTest():
            new_dbc = self._dbc.copy()
            with self.assertRaises(OperationalError):
                with new_dbc.cursor() as cur:
                    cur.execute(SELECT_FROM_GALAXY)


if __name__ == "__main__":
    unittest.main()
