import conn_util

print(len(conn_util.execute_query("show tables", db_name="test_analyze")))

