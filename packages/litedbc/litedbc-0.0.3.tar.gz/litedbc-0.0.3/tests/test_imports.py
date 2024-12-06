import unittest


class TestImports(unittest.TestCase):

    def test_import_classes(self):
        try:
            # import classes
            from litedbc import LiteDBC
            from litedbc import ColumnInfo
            from litedbc import Transaction
            from litedbc import Cursor
            # import enums
            from litedbc import TransactionMode
            from litedbc import LockingMode
            from litedbc import JournalMode
            from litedbc import SyncMode
            # import errors
            from litedbc.errors import Error
            from litedbc.errors import InterfaceError
            from litedbc.errors import DatabaseError
            from litedbc.errors import DataError
            from litedbc.errors import OperationalError
            from litedbc.errors import IntegrityError
            from litedbc.errors import InternalError
            from litedbc.errors import ProgrammingError
            from litedbc.errors import NotSupportedError
        except ImportError:
            self.assertTrue(False)


if __name__ == "__main__":
    unittest.main()
