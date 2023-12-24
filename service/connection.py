import clickhouse_driver

connection= clickhouse_driver.connect(
  host='127.0.0.1',
  # host='172.20.10.4',
  port='9000',
  user='default',
  #password,
  database='kpe'
)


