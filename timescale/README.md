# Timescale

## Install
- [Install self-hosted TimescaleDB from source](https://docs.timescale.com/install/latest/self-hosted/installation-source/#configure-postgresql-after-installing-from-source)

## Troubleshooting
```
CMake Error at CMakeLists.txt:535 (message):
  Could not find pg_config.h in /usr/include/postgresql.  Make sure PG_PATH
  points to a valid PostgreSQL installation that includes development
  headers.
```
- [Compile timescaledb source code on debian10 arm64](https://stackoverflow.com/questions/64747925/compile-timescaledb-source-code-on-debian10-arm64)
```
/usr/include/postgresql/13/server/libpq/libpq-be.h:34:10: fatal error: gssapi/gssapi.h: No such file or directory
 #include <gssapi/gssapi.h>
          ^~~~~~~~~~~~~~~~~
compilation terminated.
```
- [pynfs: error: gssapi/gssapi.h: No such file or directory](https://stackoverflow.com/questions/20992032/pynfs-error-gssapi-gssapi-h-no-such-file-or-directory)

```
the files belonging to this database system will be owned by user "postgres". this user must also own the server process. 
```
- [Trying to get Postgres setup in my environment but can't seem to get permissions to intidb](https://stackoverflow.com/questions/10431426/trying-to-get-postgres-setup-in-my-environment-but-cant-seem-to-get-permissions)

```
initdb: error: invalid locale settings; check lang and lc_* environment variables
```
- [initdb.bin: invalid locale settings; check LANG and LC_* environment variables](https://stackoverflow.com/questions/41956994/initdb-bin-invalid-locale-settings-check-lang-and-lc-environment-variables)

## Setup
```console
$ docker build -t timescaledb .
$ docker run -d -e POSTGRES_PASSWORD=$PASSWORD -p 5432:5432 --name timescaledb timescaledb
$ docker exec -it timescaledb sed -i "s/shared_preload_libraries = ''/shared_preload_libraries = 'timescaledb'/" /var/lib/postgresql/data/postgresql.conf
$ docker restart timescaledb
$ docker exec -it timescaledb psql -U postgres
psql (13.9 (Debian 13.9-1.pgdg110+1))
Type "help" for help.

postgres=# CREATE EXTENSION IF NOT EXISTS timescaledb;
WARNING:  
WELCOME TO
 _____ _                               _     ____________  
|_   _(_)                             | |    |  _  \ ___ \ 
  | |  _ _ __ ___   ___  ___  ___ __ _| | ___| | | | |_/ / 
  | | | |  _ ` _ \ / _ \/ __|/ __/ _` | |/ _ \ | | | ___ \ 
  | | | | | | | | |  __/\__ \ (_| (_| | |  __/ |/ /| |_/ /
  |_| |_|_| |_| |_|\___||___/\___\__,_|_|\___|___/ \____/
               Running version 2.9.1
For more information on TimescaleDB, please visit the following links:

 1. Getting started: https://docs.timescale.com/timescaledb/latest/getting-started
 2. API reference documentation: https://docs.timescale.com/api/latest
 3. How TimescaleDB is designed: https://docs.timescale.com/timescaledb/latest/overview/core-concepts

Note: TimescaleDB collects anonymous reports to better understand and assist our users.
For more information and how to disable, please see our docs https://docs.timescale.com/timescaledb/latest/how-to-guides/configuration/telemetry.

CREATE EXTENSION
postgres=# \dx
                                    
                                      List of installed extensions
    Name     | Version |   Schema   |                            Description                            
-------------+---------+------------+-------------------------------------------------------------------
 plpgsql     | 1.0     | pg_catalog | PL/pgSQL procedural language
 timescaledb | 2.9.1   | public     | Enables scalable inserts and complex queries for time-series data
(2 rows)
```



## Data
- daily
- minutely
- secondly