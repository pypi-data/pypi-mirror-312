import os
import pathlib
from litedbc import const, errors


def is_stmt(name, sql):
    sql = sql.lstrip()
    if len(sql) < len(name):
        return False
    return name.upper() == sql[:len(name)].upper()


def match(alpha_dbc, beta_dbc):
    """Match two database via their connectors.
    All tables defined in alpha_dbc should be in beta_dbc that might have additional tables."""
    for ref_table in alpha_dbc.list_tables():
        alpha_cols = alpha_dbc.inspect(ref_table)
        try:
            beta_cols = beta_dbc.inspect(ref_table)
        except errors.Error as e:
            return False
        n = len(alpha_cols)
        if n != len(beta_cols):
            return False
        for i in range(n):
            if alpha_cols[i] != beta_cols[i]:
                return False
    return True


def ensure_db_filename(filename):
    filename = filename if filename else ":memory:"
    if filename == ":memory:" or filename.startswith("file:"):
        return filename
    return str(pathlib.Path(filename).resolve())


def ensure_parent_dir(filename):
    try:
        os.makedirs(os.path.dirname(filename))
    except FileExistsError:
        pass


def get_start_transaction_stmt(isolation_level):
    isolation_level = isolation_level.value.upper()
    if isolation_level not in const.TransactionMode:
        msg = "Invalid isolation level '{}'".format(isolation_level)
        raise errors.Error(msg)
    return "BEGIN {}".format(isolation_level)


def get_readonly_value(filename, is_readonly):
    if (filename.startswith("file:") and
            ("?mode=ro" in filename or "&mode=ro" in filename)):
        return True
    return is_readonly
