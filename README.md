# jimiPlugin: database

A JIMI Plugin for interacting with various databases. Currently supports MSSQL and Oracle.

## Pre-requisites
Requires ODBC Drivers to communicate. These drivers can be configured within the settings file for JIMI like so:
```
  "databasePlugin": {
      "mssqlDriver" : "ODBC Driver 17 for SQL Server",
      "oracleDriver" : "ODBC Driver for Oracle"
  },
```
This must match the names you have configured inside your odbcinst.ini file.

For Oracle, this resource is useful: https://github.com/mkleehammer/pyodbc/wiki/Connecting-to-Oracle-from-RHEL-or-Centos

For MSSQL, follow this: https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15
