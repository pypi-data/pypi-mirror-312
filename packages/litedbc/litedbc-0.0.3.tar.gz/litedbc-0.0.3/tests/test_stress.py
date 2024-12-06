import unittest
import os
import os.path
import random
import tempfile
from time import sleep
from litedbc import LiteDBC
from asyncpal import ThreadPool


# ---- CONFIG
MAX_INSERTIONS = 64
IDLE_TIMEOUT = 0.001  # seconds
VERBOSE = False

# ----

INIT_SCRIPT = """
-- Create the ELEMENT table
CREATE TABLE element (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    state INTEGER NOT NULL);"""

INSERT_ELEMENT = "INSERT INTO element (state) VALUES (?)"
SELECT_ELEMENTS = "SELECT * FROM element"
UPDATE_ELEMENT = "UPDATE element SET state=? WHERE id=?"
DELETE_ELEMENT = "DELETE FROM element WHERE id=?"


def insert_element(dbc):
    for _ in range(MAX_INSERTIONS):
        sleep(IDLE_TIMEOUT)
        with dbc.cursor() as cur:
            cur.execute(INSERT_ELEMENT, (0, ))
            if VERBOSE:
                print("INSERTED:\t{}\t\t(OK)".format(cur.lastrowid), flush=True)
    return True


def update_element(dbc, old_state, new_state):
    i = 0
    while i < MAX_INSERTIONS:
        sleep(IDLE_TIMEOUT)
        with dbc.transaction() as cur:
            cur.execute(SELECT_ELEMENTS)
            r = cur.fetchall()
            if not r:
                continue
            item = random.choice(r)
            item_id, state = item
            if state == old_state:
                cur.execute(UPDATE_ELEMENT, (new_state, item_id))
                if VERBOSE:
                    print("UPDATED: \t{}\t\t(OK)".format(item_id), flush=True)
                i += 1
    return True


def check_isolation(dbc):
    for _ in range(MAX_INSERTIONS):
        sleep(IDLE_TIMEOUT)
        with dbc.transaction() as cur:
            cur.execute(SELECT_ELEMENTS)
            r1 = cur.fetchall()
            sleep(IDLE_TIMEOUT + 0.001)
            cur.execute(SELECT_ELEMENTS)
            r2 = cur.fetchall()
            assert r1 == r2
            if VERBOSE:
                print("ISOLATION\t\t\t(OK)")
    return True


def delete_element(dbc, target_state):
    i = 0
    while i < MAX_INSERTIONS:
        sleep(IDLE_TIMEOUT)
        with dbc.transaction() as cur:
            cur.execute(SELECT_ELEMENTS)
            r = cur.fetchall()
            if not r:
                continue
            item = random.choice(r)
            item_id, state = item
            if state == target_state:
                cur.execute(DELETE_ELEMENT, (item_id, ))
                if VERBOSE:
                    print("DELETED: \t{}\t\t(OK)".format(item_id), flush=True)
                i += 1
    return True


class StressTest(unittest.TestCase):
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
        if VERBOSE:
            print("LiteDBC Stress Test")
            print("===================")
            print()
        with ThreadPool(5) as pool:
            future_1 = pool.submit(insert_element, self._dbc)
            future_2 = pool.submit(update_element, self._dbc, 0, 1)
            future_3 = pool.submit(update_element, self._dbc, 1, 2)
            future_4 = pool.submit(check_isolation, self._dbc)
            future_5 = pool.submit(delete_element, self._dbc, 2)
            self.assertTrue(future_1.collect())
            self.assertTrue(future_2.collect())
            self.assertTrue(future_3.collect())
            self.assertTrue(future_4.collect())
            self.assertTrue(future_5.collect())
        with self._dbc.cursor() as cur:
            cur.execute(SELECT_ELEMENTS)
            self.assertEqual(0, len(cur.fetchall()))


if __name__ == "__main__":
    unittest.main()
