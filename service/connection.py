import clickhouse_driver

connection= clickhouse_driver.connect(
  # host='192.168.0.9',
  host='172.20.10.2',
  port='9000',
  user='default',
  #password,
  database='kpe'
)


