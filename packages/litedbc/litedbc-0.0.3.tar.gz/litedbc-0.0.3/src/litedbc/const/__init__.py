from enum import Enum, unique


# Mandatory globals (DB-API)
# https://peps.python.org/pep-0249/#threadsafety
# https://peps.python.org/pep-0249/#apilevel
# https://peps.python.org/pep-0249/#paramstyle
threadsafety = 2  # Threads may share the module and connections.
apilevel = "2.0"
paramstyle = "qmark"  # The `named` DB-API parameter style is also supported.


@unique
class TransactionMode(Enum):
    DEFERRED = "DEFERRED"
    IMMEDIATE = "IMMEDIATE"
    EXCLUSIVE = "EXCLUSIVE"


@unique
class LockingMode(Enum):
    NORMAL = "NORMAL"
    EXCLUSIVE = "EXCLUSIVE"


@unique
class SyncMode(Enum):
    EXTRA = "EXTRA"
    FULL = "FULL"
    NORMAL = "NORMAL"
    OFF = "OFF"


@unique
class JournalMode(Enum):
    DELETE = "DELETE"
    TRUNCATE = "TRUNCATE"
    PERSIST = "PERSIST"
    MEMORY = "MEMORY"
    WAL = "WAL"
    OFF = "OFF"
