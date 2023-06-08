import pymysql
import conf
import socket


def get_mysql_conn(db_name=conf.db_name):
    return pymysql.connect(
        user=conf.user,
        host=conf.ip,
        db=db_name,
        port=conf.port
    )


def fetch_one(cursor):
    return cursor.fetchone()


def fetch_all(cursor):
    return cursor.fetchall()


def execute_query(sql: str, fetch=fetch_all, enable_stats_check=True, db_name=conf.db_name):
    conn = get_mysql_conn(db_name)
    try:
        with conn.cursor() as cursor:
            cursor.execute("SET enable_nereids_planner=true")
            cursor.execute("SET enable_fallback_to_original_planner=false")
            if enable_stats_check:
                cursor.execute("SET forbid_unknown_col_stats=True")
            else:
                cursor.execute("SET forbid_unknown_col_stats=False")
            cursor.execute(sql)
            return fetch(cursor)
    except BaseException as e:
        print("Failed to execute " + sql)
        raise e
    finally:
        conn.close()


def is_port_open(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.settimeout(1)  # Set a timeout value for the connection attempt
        result = sock.connect_ex((host, port))
        if result == 0:
            return True  # Port is open
        else:
            return False  # Port is closed or blocked
    finally:
        sock.close()


def fetch_one_with_wrapp(cursor):
    row = cursor.fetchone()

    # Get column names from cursor description
    columns = [desc[0] for desc in cursor.description]

    # Create a dictionary of field names and values
    return dict(zip(columns, row))


def fetchall_with_wrapp(cursor):
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    row_list = []
    for row in rows:
        row_list.append(dict(zip(columns, row)))
    return row_list
