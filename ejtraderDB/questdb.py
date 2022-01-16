#!/usr/bin/env python
# File:         PyQDB.py
# Description:  Main class - QuestDB API wrapper for Python
# Author:       Jakob Schaffarczyk <jakobs[᠎at]js-on.de>
# Date:         08.12.2021
# Version:      0.0.1

from posixpath import sep
from typing import Any, Union
import requests
from qdb_api import API, restricted_chars
import sys
import os
from urllib.parse import quote_plus
import pandas as pd


class QuestDB:
    def __init__(self, base_url: str = "http://127.0.0.1:9000"):
        """Init QuestDB Class

        Args:
            base_url (str, optional): API URL for QuestDB. Defaults to "http://127.0.0.1:9000".
        """
        self.session: requests.Session = requests.Session()
        self.url: str = base_url

    def imp(self,
            filename: str,
            atomicity: API["imp"]["atomicity"]["type"] = API["imp"]["atomicity"]["default"],
            commitLag: API["imp"]["commitLag"]["type"] = API["imp"]["commitLag"]["default"],
            durable: API["imp"]["durable"]["type"] = API["imp"]["durable"]["default"],
            fmt: API["imp"]["fmt"]["type"] = API["imp"]["fmt"]["default"],
            forceHeader: API["imp"]["forceHeader"]["type"] = API["imp"]["forceHeader"]["default"],
            maxUncommittedRows: API["imp"]["maxUncommittedRows"]["type"] = API["imp"]["maxUncommittedRows"]["default"],
            name: API["imp"]["name"]["type"] = API["imp"]["name"]["default"],
            overwrite: API["imp"]["overwrite"]["type"] = API["imp"]["overwrite"]["default"],
            partitionBy: API["imp"]["partitionBy"]["type"] = API["imp"]["partitionBy"]["default"],
            skipLev: API["imp"]["skipLev"]["type"] = API["imp"]["skipLev"]["default"],
            timestamp: API["imp"]["timestamp"]["type"] = API["imp"]["timestamp"]["default"]) -> Union[dict, str]:
        """
        /imp streams tabular text data directly into a table. It supports CSV, TAB and pipe (|) delimited inputs with optional headers. There are no restrictions on data size. Data types and structures are detected automatically, without additional configuration. In some cases, additional configuration can be provided to improve the automatic detection as described in [user-defined schema](https://questdb.io/docs/reference/api/rest/#user-defined-schema).

        Args:
            `atomicity (int, optional)`: 0: The entire file will be skipped. 1: The row is skipped. 2: The column is skipped.

            `commitLag (int, optional)`: Commit lag of the import in µs precision (e.g. 2 minutes is expressed as 120000000, 120 followed by 6 zeros). For context see the commit lag guide (https://questdb.io/docs/guides/out-of-order-commit-lag/).

            `durable (bool, optional)`: true or false. When set to true, import will be resilient against OS errors or power losses by forcing the data to be fully persisted before sending a response back to the user.

            `fmt (str, optional)`: Can be set to json to get the response formatted as such.

            `forceHeader (bool, optional)`: true or false. When false, QuestDB will try to infer if the first line of the file is the header line. When set to true, QuestDB will expect that line to be the header file.

            `maxUncommittedRows (int, optional)`: The maximum number of uncommitted rows to keep in memory before triggering a sort and commit operation. For context, see the commit lag guide (https://questdb.io/docs/guides/out-of-order-commit-lag/).

            `name (str, optional)`: Name of the table to create, see: https://questdb.io/docs/reference/api/rest/#names

            `overwrite (bool, optional)`: true or false. When set to true, any existing data or structure will be overwritten.

            `partitionBy (str, optional)`: See partitions: https://questdb.io/docs/concept/partitions/#properties

            `skipLev (bool, optional)`: true or false. Skip \Line Extra Values\, when set to true, the parser will ignore those extra values rather than ignoring entire line. An extra value is something in addition to what is defined by the header.

            `timestamp (str, optional)`: Name of the column that will be used as a designated timestamp (https://questdb.io/docs/concept/designated-timestamp/).

        Returns:
            Union[str, dict]: Response in 'tabular' form or 'JSON', depending on 'fmt' parameter (defaults to 'tabular')
        """
        # API URL
        url: str = f"{self.url}/imp?"

        # Structured input parameters/values
        parameters: dict = {
            "atomicity": atomicity,
            "commitLag": commitLag,
            "durable": durable,
            "fmt": fmt,
            "forceHeader": forceHeader,
            "maxUncommittedRows": maxUncommittedRows,
            "name": name,
            "overwrite": overwrite,
            "partitionBy": partitionBy,
            "skipLev": skipLev,
            "timestamp": timestamp
        }

        # Check if CSV file exists
        if not os.path.exists(filename):
            print(f"File '{filename} does not exist on the system.")
            sys.exit(1)

        # Iterative check of all parameters
        for k, v in parameters.items():
            if not self._check("imp", k, v):
                self._not_compliant("imp", k)
            else:
                if v != API["imp"][k]["default"]:
                    url += f"{k}={v}&"
        if url.endswith("&"):
            url = url[:-1]

        # send request
        files: dict = {"data": open(filename, "rb")}
        res: requests.Response = self.session.request(
            API["imp"]["method"], url=url, files=files)
        if fmt == "tabular":
            return res.text
        elif fmt == "json":
            return res.json()

    def exec(self,
             count: API["exec"]["count"]["type"] = API["exec"]["count"]["default"],
             limit: API["exec"]["limit"]["type"] = API["exec"]["limit"]["default"],
             nm: API["exec"]["nm"]["type"] = API["exec"]["nm"]["default"],
             query: API["exec"]["query"]["type"] = API["exec"]["query"]["default"],
             timings: API["exec"]["timings"]["type"] = API["exec"]["timings"]["default"]) -> list:
        """`/exec` compiles and executes the `SQL` query supplied as a parameter and returns a JSON response.
        `/exec` is expecting an HTTP `GET` request with following query parameters:

        Args:
            `count (bool, optional)`: `true` or `false`. Counts the number of rows and returns this value.

            `limit (str, optional)`: Allows limiting the number of rows to return. limit=10 will return the first 10 rows (equivalent to limit=1,10), limit=10,20 will return row numbers 10 through to 20 inclusive.

            `nm (bool, optional)`: `true` or `false`. Skips the metadata section of the response when set to true.

            `query (str)`: URL encoded query text. It can be multi-line.

            `timings (bool, optional)`: `true` or false. When set to `true`, QuestDB will also include a timings property in the response which gives details about the execution.

        Returns:
            dict: JSON response
        """
        # API URL
        url: str = f"{self.url}/exec?"

        # Structured input parameters/values
        parameters: dict = {
            "count": count,
            "limit": limit,
            "nm": nm,
            "query": quote_plus(query),
            "timings": timings
        }

        # Iterative check of all parameteres
        for k, v in parameters.items():
            if not self._check("exec", k, v):
                self._not_compliant("exec", k)
            else:
                if v != API["exec"][k]["default"]:
                    url += f"{k}={v}&"
        if url.endswith("&"):
            url = url[:-1]

        # send request
        res: requests.Response = self.session.request(
            API["exec"]["method"], url=url)
        return res.json()

    def exp(self,
            limit: API["exp"]["limit"]["type"] = API["exp"]["limit"]["default"],
            query: API["exp"]["query"]["type"] = API["exp"]["query"]["default"],
            output: API["exp"]["format"]["type"] = API["exp"]["format"]["default"],
            separator: str = ",") -> Union[pd.DataFrame, str]:
        """This endpoint allows you to pass url-encoded queries but the request body is returned in a tabular form to be saved and reused as opposed to JSON.

        Args:
            `limit (str, optional)`: Paging opp parameter. For example, limit=10,20 will return row numbers 10 through to 20 inclusive and limit=20 will return first 20 rows, which is equivalent to limit=0,20. limit=-20 will return the last 20 rows.

            `query (str)`: URL encoded query text. It can be multi-line.

            `output (str)`: Format to export data to. `csv` and `pandas` DataFrame supported. Default is `csv`.

            `separator (str)`: CSV seperator (needed to properly format export data)

        Returns:
            Union[pd.DataFrame, str]: Exported data in requested format.
        """
        # API URL
        url: str = f"{self.url}/exp?"

        # Structured input parameters/values
        parameters: dict = {
            "limit": limit,
            "query": quote_plus(query)
        }

        # Iterative check of all parameters
        for k, v in parameters.items():
            if not self._check("exp", k, v):
                self._not_compliant("exp", k)
            else:
                if v != API["exp"][k]["default"]:
                    url += f"{k}={v}&"
        if url.endswith("&"):
            url = url[:-1]

        # send request
        res: requests.Response = self.session.request(
            API["exec"]["method"], url=url)

        # output as CSV
        if output == "csv":
            return res.text
        # output as Pandas DataFrame
        elif output == "pandas":
            csv = res.text.split("\r\n")
            data = []
            columns = [i.strip('"').strip(" ")
                       for i in csv[0].split(separator)]
            for line in csv[1:]:
                if line == '':
                    continue
                t = [self._assign_vartype(i.strip('"').strip(" "))
                     for i in line.split(separator)]
                data.append(t)

            df = pd.DataFrame(data, columns=columns)
            return df

    def _assign_vartype(self, value: str) -> Any:
        """Assign correct variable type to var

        Args:
            value (str): original value

        Returns:
            Any: casted value
        """
        for t in [float, int, str]:
            try:
                casted = t(value)
                return casted
            except:
                pass

    def _not_compliant(self, route: str, parameter: str):
        """Print error message if parameter is not compliant to API requirements

        Args:
            route (str): API route
            parameter (str): Corrupted parameter
        """
        print(
            f"Value for '{parameter}' does not comply with the API definition.")
        self.help(route, parameter)

    def help(self, route: str, parameter: str):
        """Print description for request param taken from the official documentation and exit

        Args:
            route (str): API route (/imp, /exec, /exp)
            parameter (str): Request parameter (eg. fmt, query, ...)
        """
        try:
            print(API[route][parameter]["description"])
        except:
            print(
                f"Route /{route} does not have any valid {API[route]['method']} parameter called {parameter}")
        sys.exit(1)

    def _contains_restricted_char(self, value):
        """Check if value contains characters not accepted by QuestDB API

        Args:
            value ([type]): Value to check
        """
        if type(value) != str:
            return
        for c in str(value):
            if c in restricted_chars:
                print(
                    f"[i] Restricted character '{c}' will be automatically removed!")

    def _check(self, route: str, parameter: str, value) -> bool:
        """Check if parameter is mandatory and valid

        Args:
            route (str): API route
            parameter (str): Name of the parameter
            value ([type]): Value of the parameter

        Returns:
            bool: if value is valid or not
        """
        mandatory: bool = API[route][parameter]["required"]
        fnct: function = API[route][parameter]["check"]
        ptype: Any = API[route][parameter]["type"]
        if mandatory and value == API[route][parameter]["default"]:
            print(f"[!] Parameter '{parameter}' is mandatory!")
            sys.exit(1)
        if parameter != "query":
            self._contains_restricted_char(value)
        return fnct(value) and type(value) == ptype
