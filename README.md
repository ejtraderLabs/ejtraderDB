![Pypi Publish](https://github.com/ejtraderLabs/ejtraderDB/actions/workflows/python-publish.yml/badge.svg)
[![Release](https://img.shields.io/github/v/release/ejtraderLabs/ejtraderDB)](https://github.com/ejtraderLabs/ejtraderDB/releases/latest)
[![License](https://img.shields.io/github/license/ejtraderLabs/ejtraderDB)](https://github.com/ejtraderLabs/ejtraderDB/blob/master/LICENSE)

## Install requirements:

```sh
pip install ejtraderDB - U
```

### Description for DictSQlite

## import

```python
from ejtraderDB import DictSQlite

api = DictSQLite('history',multithreading=True)


# save to sqlite
api["keyname"] = dataFrame


# read from sqlite

dataFrame = api['keyname']

print(dataFrame)
```


## Description for QuestDb

API wrapper following the basic API requirements of QuestDB described [here](https://questdb.io/docs/reference/api/rest/).

## Import

```python
from ejtraderDB import QuestDB

api = QuestDB()
```

## Methods

### /imp - Import

*`/imp` streams tabular text data directly into a table. It supports CSV, TAB and pipe (`|`) delimited inputs with optional headers. There are no restrictions on data size. Data types and structures are detected automatically, without additional configuration. In some cases, additional configuration can be provided to improve the automatic detection as described in [user-defined schema](https://questdb.io/docs/reference/api/rest/#user-defined-schema).*

```py
res = api.imp(filename="test.csv", name="ejtraderDB")
```

> See `qdb_api.py` or [API reference](https://questdb.io/docs/reference/api/rest/#imp---import-data) for all possible parameters.

### /exec - Execute queries

*`/exec` compiles and executes the SQL query supplied as a parameter and returns a JSON response.*

```py
res = api.exec(query="SELECT * FROM ejtraderDB")
```

**SQL queries will be verified via `sqlvalidator==0.0.17` there might be issues with QuestDB SQL Syntax.**

> See `qdb_api.py` or [API reference](https://questdb.io/docs/reference/api/rest/#exec---execute-queries) for all possible parameters.

### /exp - Export data

*This endpoint allows you to pass url-encoded queries but the request body is returned in a tabular form to be saved and reused as opposed to JSON.*

```py
res = api.exp(query="SELECT * FROM ejtraderDB")
```

## you can now choose between the following output formats:
- CSV: `qdb.exp(query="...", output="csv")`
- DataFrame: `qdb.exp(query="...", output="pandas"`

> See `qdb_api.py` or [API reference](https://questdb.io/docs/reference/api/rest/#exp---export-data) for all possible parameters.
