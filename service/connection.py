import clickhouse_driver

connection= clickhouse_driver.connect(
  host='192.168.0.9',
  port='9000',
  user='default',
  #password,
  database='kpe'
)


