[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI package version](https://img.shields.io/pypi/v/litedbc)](https://pypi.org/project/litedbc)
[![Downloads](https://static.pepy.tech/badge/litedbc)](https://pepy.tech/project/litedbc)


<!-- Intro Text -->
# LiteDBC
<b>Lightweight Database Connector</b>

This library is a streamlined wrapper for Python's [sqlite3](https://docs.python.org/3/library/sqlite3.html) module, built to provide a user-friendly and thread-safe bridge between [Jinbase](https://github.com/pyrustic/jinbase) and [SQLite](https://www.sqlite.org/index.html).

**Connecting to an embedded database:**

```python
from litedbc import LiteDBC

dbc = LiteDBC("/path/to/file.db")

# manually initialize the database with a SQL script
if dbc.is_new:
    with dbc.transaction() as cursor:
        cursor.execute_script("-- <Initialization SQL Script> --")
# ...
dbc.close()
# the line above is optional, as the connection 
# closes automatically when the program exits
```

<p align="right"><a href="#readme">Back to top</a></p>

**Providing SQL script for automatic initialization:**

```python
from litedbc import LiteDBC

INIT_SCRIPT = """BEGIN TRANSACTION;
-- Create the USER table
CREATE TABLE user (
    name TEXT PRIMARY KEY,
    age INTEGER NOT NULL);
COMMIT;"""

with LiteDBC("/path/to/file.db", init_script=INIT_SCRIPT) as dbc:
    pass
```

<p align="right"><a href="#readme">Back to top</a></p>

**Interacting with a database:**

```python
from litedbc import LiteDBC

with LiteDBC("/path/to/file.db") as dbc:
    with dbc.cursor() as cur:
        # execute a SQL statement
        statement = "INSERT INTO user (id, name) VALUES (?, ?)"
        cur.execute(statement, (42, "alex"))  # returns the 'rowcount'
        
        # query data
        cur.execute("SELECT id, name FROM user")
        
        # get the rows iteratively
        for row in cur.fetch():
            print(row)
        
        # execute a SQL script in a single transaction
        cur.executescript("-- SQL Script --")
```

<p align="right"><a href="#readme">Back to top</a></p>

**Creating a transaction context to run complex logic:**

```python
from litedbc import LiteDBC

dbc = LiteDBC("/path/to/file.db")

# creating a transaction context
with dbc.transaction() as cur:  # accepts an optional transaction mode
    # from here, everything will be executed within a single transaction
    cur.execute("SELECT COUNT(*) FROM user")
    for row in cur.fetch():
        if row[0] >= 256:
            cur.execute("DELETE FROM user WHERE id=?", (1,))

dbc.close()
```

<p align="right"><a href="#readme">Back to top</a></p>

**Miscelleaneous:**

```python
from litedbc import LiteDBC

# the constructor also accepts conn_kwargs, on_create_db, on_create_conn
dbc = LiteDBC("/path/to/file.db")  # not filename provided -> in-memory db !

# return a tuple of tables present in the database
tables = dbc.list_tables()

# return a list of ColumnInfo instances that provide rich info
# about each column, such as whether it's a primary key column or not
table_info = dbc.inspect(table)

# export the database as a SQL script
sql_script = dbc.dump(dst=None)

# safely create a backup
dbc.backup("/path/to/file.backup")

# create a new instance of Dbc for the same database file
new_dbc = dbc.copy()

# Note that the Dbc class also exposes these properties:
# .new, .conn, .in_memory, .filename, .conn_kwargs, .closed, .deleted
```

<p align="right"><a href="#readme">Back to top</a></p>


# Testing and contributing
Feel free to **open an issue** to report a bug, suggest some changes, show some useful code snippets, or discuss anything related to this project. You can also directly email [me](https://pyrustic.github.io/#contact).

## Setup your development environment
Following are instructions to setup your development environment

```bash
# create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# clone the project then change into its directory
git clone https://github.com/pyrustic/litedbc.git
cd litedbc

# install the package locally (editable mode)
pip install -e .

# run tests
python -m tests

# deactivate the virtual environment
deactivate
```

<p align="right"><a href="#readme">Back to top</a></p>

# Installation
**LiteDBC** is **cross-platform**. It is built on [Ubuntu](https://ubuntu.com/download/desktop) and should work on **Python 3.8** or **newer**.

## Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate
```

## Install for the first time

```bash
pip install litedbc
```

## Upgrade the package
```bash
pip install litedbc --upgrade --upgrade-strategy eager
```

## Deactivate the virtual environment
```bash
deactivate
```

<p align="right"><a href="#readme">Back to top</a></p>

# About the author
Hello world, I'm Alex, a tech enthusiast ! Feel free to get in touch with [me](https://pyrustic.github.io/#contact) !

<br>
<br>
<br>

[Back to top](#readme)
