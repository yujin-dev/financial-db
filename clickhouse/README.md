# Setup
## AWS instance setup
storage는 HDD(aws volume `st1`)을 적용합니다

### Mount HDD storage
```bash
sudo file -s /dev/sdb
sudo lsblk -f
# sudo mkfs -t xfs /dev/sdb
sudo mkdir /data
sudo mount /dev/sdb /data
```

### Connect Instance
```
ssh -i {pem-file} {instance-ip}
```

## Clickhouse Quick Install 
```
curl https://clickhouse.com/ | sh
sudo ./clickhouse install
```
### Start Server
```
sudo clickhouse start
```
`sudo  /usr/bin/clickhouse-server --config-file /etc/clickhouse-server/config.xml --pid-file /var/run/clickhouse-server/clickhouse-server.pid`로 로그를 확인하면서 디버깅이 가능하다 

## Connect Clickhouse
```
clickhouse client
```

## Dump Data From S3
```
s3(path, [aws_access_key_id, aws_secret_access_key,] [format, [structure, [compression]]])
```
- [S3 Table Functions](https://clickhouse.com/docs/en/integrations/s3/s3-table-functions)
    > The s3 table function allows us to read and write files from and to S3 compatible storage
