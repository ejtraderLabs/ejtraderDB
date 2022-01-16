#!/usr/bin/env python
# File:         PyQDB.py
# Description:  API restrictions for QuestDB REST API
# Author:       Jakob Schaffarczyk <jakobs[᠎at]js-on.de>
# Date:         08.12.2021
# Version:      0.0.1

from re import match
from sqlvalidator import sql_validator

restricted_chars = [" ", ".", "?", ",", ":", "\\", "/",
                    "\\\\", "\0", ")", "(", "_", "+", "-", "*", "~", "%"]

API = {
    "imp": {
        "method": "POST",
        "atomicity": {
            "required": False,
            "default": 2,
            "check": lambda x: x in [0, 1, 2],
            "type": int,
            "description": "0: The entire file will be skipped. 1: The row is skipped. 2: The column is skipped"
        },
        "commitLag": {
            "required": False,
            "default": 0,
            "check": lambda x: x >= 0,
            "type": int,
            "description": "Commit lag of the import in µs precision (e.g. 2 minutes is expressed as 120000000, 120 followed by 6 zeros). For context see the commit lag guide (https://questdb.io/docs/guides/out-of-order-commit-lag/)."
        },
        "durable": {
            "required": False,
            "default": False,
            "check": lambda x: type(x) == bool,
            "type": bool,
            "description": "true or false. When set to true, import will be resilient against OS errors or power losses by forcing the data to be fully persisted before sending a response back to the user."
        },
        "fmt": {
            "required": False,
            "default": "tabular",
            "check": lambda x: x in ["tabular", "json"],
            "type": str,
            "description": "Can be set to json to get the response formatted as such."
        },
        "forceHeader": {
            "required": False,
            "default": False,
            "check": lambda x: type(x) == bool,
            "type": bool,
            "description": "true or false. When false, QuestDB will try to infer if the first line of the file is the header line. When set to true, QuestDB will expect that line to be the header file."
        },
        "maxUncommittedRows": {
            "required": False,
            "default": 0,
            "check": lambda x: x >= 0,
            "type": int,
            "description": "The maximum number of uncommitted rows to keep in memory before triggering a sort and commit operation. For context, see the commit lag guide (https://questdb.io/docs/guides/out-of-order-commit-lag/)."
        },
        "name": {
            "required": False,
            "default": "test",
            "check": lambda x: str(x) != "",
            "type": str,
            "description": "Name of the table to create, see: https://questdb.io/docs/reference/api/rest/#names"
        },
        "overwrite": {
            "required": False,
            "default": False,
            "check": lambda x: type(x) == bool,
            "type": bool,
            "description": "true or false. When set to true, any existing data or structure will be overwritten."
        },
        "partitionBy": {
            "required": False,
            "default": "NONE",
            "check": lambda x: x in ["NONE", "YEAR", "MONTH", "DAY", "HOUR"],
            "type": str,
            "description": "See partitions: https://questdb.io/docs/concept/partitions/#properties"
        },
        "skipLev": {
            "required": False,
            "default": False,
            "check": lambda x: type(x) == bool,
            "type": bool,
            "description": "true or false. Skip \"Line Extra Values\", when set to true, the parser will ignore those extra values rather than ignoring entire line. An extra value is something in addition to what is defined by the header."
        },
        "timestamp": {
            "required": False,
            "default": "ts",
            "check": lambda x: str(x) != "",
            "type": str,
            "description": "Name of the column that will be used as a designated timestamp (https://questdb.io/docs/concept/designated-timestamp/)."
        }
    },
    "exec": {
        "method": "GET",
        "count": {
            "required": False,
            "default": False,
            "check": lambda x: type(x) == bool,
            "type": bool,
            "description": "True or false. Counts the number of rows and returns this value."
        },
        "limit": {
            "required": False,
            "default": "10",
            "check": lambda x: True if match(r'^\d+,?\d*$', x) else False,
            "type": str,
            "description": "Allows limiting the number of rows to return. limit=10 will return the first 10 rows (equivalent to limit=1,10), limit=10,20 will return row numbers 10 through to 20 inclusive."
        },
        "nm": {
            "required": False,
            "default": False,
            "check": lambda x: type(x) == bool,
            "type": bool,
            "description": "true or false. Skips the metadata section of the response when set to true."
        },
        "query": {
            "required": True,
            "default": "",
            "check": lambda x: sql_validator.parse(x).is_valid(),
            "type": str,
            "description": "URL encoded query text. It can be multiline."
        },
        "timings": {
            "required": False,
            "default": False,
            "check": lambda x: type(x) == bool,
            "type": bool,
            "description": "true or false. When set to true, QuestDB will also include a timings property in the response which gives details about the execution."
        }
    },
    "exp": {
        "method": "GET",
        "limit": {
            "required": False,
            "default": "10",
            "check": lambda x: True if match(r'^\d+,?\d*$', x) else False,
            "type": str,
            "description": "Paging opp parameter. For example, limit=10,20 will return row numbers 10 through to 20 inclusive and limit=20 will return first 20 rows, which is equivalent to limit=0,20. limit=-20 will return the last 20 rows."
        },
        "query": {
            "required": True,
            "default": "",
            "check": lambda x: sql_validator.parse(x).is_valid(),
            "type": str,
            "description": "URL encoded query text. It can be multi-line."
        },
        "format": {
            "required": False,
            "default": "csv",
            "check": lambda x: x in ["csv", "pandas"],
            "type": str,
            "description": "Format to export data to. CSV and Pandas DataFrame supported."
        }
    }
}
