from __future__ import annotations
from itertools import islice, chain

SEP = "/"


def batch(iterable, size=100):
    """
    >>> list(list(_) for _ in batch(range(10), 3))
    [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    """
    it = iter(iterable)
    try:
        while True:
            batchiter = islice(it, size)
            yield chain([next(batchiter)], batchiter)
    except StopIteration:
        pass


def flat_dict(entry, sep=SEP):
    """
    flattens hierarchical dict adding sep at each depth
    """
    for key, value in entry.items():
        if isinstance(value, dict):
            for sub_key, value in flat_dict(value):
                yield key + sep + sub_key, value
        elif isinstance(value, list):
            yield key, int  # count number of items
        elif value is not None:
            yield key, type(value)


def extract_rows(data):
    """
    list all possible column names from dict
    """
    rows = {}
    for plate in data:
        rows.update(flat_dict(plate))
    return rows


def create_table_statement(
    rows: dict[str, type[int | str | float]],
    table_name: str = "report",
    column_order: list[str] | None = None,
):
    """
    :param rows: dict of `str:type`
    """
    types = {
        int: "INTEGER",
        float: "REAL",
    }
    return (
        "CREATE TABLE "
        + table_name
        + " (\n  "
        + ",\n  ".join(
            '"' + key + '" ' + types.get(rows[key], "TEXT")
            for key in column_order or sorted(rows)
        )
        + "\n)"
    )
