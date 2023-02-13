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
- docker-compose 설치 : https://soyoung-new-challenge.tistory.com/73

# Use-Case

## use hypertable
- hyperfunctions을 활용한 샘플 쿼리 : [Query the data](https://docs.timescale.com/timescaledb/latest/tutorials/financial-tick-data/financial-tick-query/)

hypertable을 생성하려면 먼저 테이블을 생성한 후 빈 테이블을 대상으로 적용한다.

## dump data
- [Logical backups with pg_dump  and pg_restore ](https://docs.timescale.com/timescaledb/latest/how-to-guides/backup-and-restore/pg-dump-and-restore/#restoring-individual-hypertables-from-backup)

보통 테이블 삽입에 비해 hypertable 삽입이 훨씬 오래 걸린다. 이를 해소하기 위해 [timescaledb-parallel-copy](https://github.com/timescale/timescaledb-parallel-copy)를 사용한다.

```console
$ pg_dump --schema-only -U {source-user} -h {source-host} -p {source-port} -t {source-table} -d {source-database} > schema.sql
$ psql -U {source-user} -h {source-host} -p {source-port} -d {source-database} -c "\COPY (SELECT * FROM source-table) TO data.csv DELIMITER ',' CSV"
$ psql -d tsdb -U postgres < schema.sql
$ psql -d tsdb -U postgres -c "SELECT create_hypertable('{table_name}', '{time_column}')"
$ psql -d tsdb -U postgres -c "\COPY table_name FROM data.csv CSV"
```

### check result
```
root@ip-172-31-45-28:/# psql -U postgres -d tsdb -c "explain analyze select * from table_name"
                                                       QUERY PLAN                                                       
------------------------------------------------------------------------------------------------------------------------
 Append  (cost=0.00..94.15 rows=1610 width=314) (actual time=0.008..0.039 rows=30 loops=1)
   ->  Seq Scan on _hyper_1_4240_chunk  (cost=0.00..12.30 rows=230 width=314) (actual time=0.007..0.008 rows=3 loops=1)
   ->  Seq Scan on _hyper_1_4241_chunk  (cost=0.00..12.30 rows=230 width=314) (actual time=0.003..0.004 rows=5 loops=1)
   ->  Seq Scan on _hyper_1_4242_chunk  (cost=0.00..12.30 rows=230 width=314) (actual time=0.003..0.004 rows=5 loops=1)
   ->  Seq Scan on _hyper_1_7016_chunk  (cost=0.00..12.30 rows=230 width=314) (actual time=0.006..0.007 rows=5 loops=1)
   ->  Seq Scan on _hyper_1_7017_chunk  (cost=0.00..12.30 rows=230 width=314) (actual time=0.002..0.003 rows=5 loops=1)
   ->  Seq Scan on _hyper_1_7018_chunk  (cost=0.00..12.30 rows=230 width=314) (actual time=0.002..0.003 rows=5 loops=1)
   ->  Seq Scan on _hyper_1_7019_chunk  (cost=0.00..12.30 rows=230 width=314) (actual time=0.004..0.004 rows=2 loops=1)
 Planning Time: 8.137 ms
 Execution Time: 0.127 ms
(10 rows)
```
