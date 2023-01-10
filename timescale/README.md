#timescale #timeseries-db #hypertable #hyperfunctions #financial-timeseries

# Install
install with docker

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

# Setup
```console
$ docker build -t timescaledb .
$ docker run -d -e POSTGRES_PASSWORD=$PASSWORD -p 5432:5432 --net host --name timescaledb timescaledb
$ docker exec -it timescaledb sed -i "s/#shared_preload_libraries = ''/shared_preload_libraries = 'timescaledb'/" /var/lib/postgresql/data/postgresql.conf
$ docker exec -it timescaledb sed -i "s/trust/md5/" /var/lib/postgresql/data/pg_hba.conf
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

### AWS Linux 2 인스턴스 활용
- docker 설치 : [Amazon ECS에서 사용할 컨테이너 이미지 생성](https://docs.aws.amazon.com/ko_kr/AmazonECS/latest/developerguide/create-container-image.html)
- troubleshooting : [Can't install docker on amazon linux instance](https://stackoverflow.com/questions/59101980/cant-install-docker-on-amazon-linux-instance)

# Use-Case

## dataset
- daily : 약 40GB의 일별 데이터 테이블을 복제하여 테스트
    - [Copy a table from one database to another in Postgres](https://stackoverflow.com/questions/3195125/copy-a-table-from-one-database-to-another-in-postgres)
- minutely
- tick
    - [kafka-crypto]

## use hypertable
- hyperfunctions을 활용한 샘플 쿼리 : [Query the data](https://docs.timescale.com/timescaledb/latest/tutorials/financial-tick-data/financial-tick-query/)

hypertable을 생성하려면 먼저 테이블을 생성한 후 빈 테이블을 대상으로 적용한다.

```console
$ pg_dump --schema-only -U {source-user} -h {source-host} -p {source-port} -t {source-table} -d {source-database} | psql -h localhost -U postgres -d tsdb
$ \SELECT create_hypertable('sec_dprc', 'datadate');
$ pg_dump --data-only -U {source-user} -h {source-host} -p {source-port} -t {source-table} -d {source-database} | psql -h localhost -U postgres -d tsdb
```

보통 테이블 삽입에 비해 hypertable 삽입이 훨씬 오래 걸린다. 