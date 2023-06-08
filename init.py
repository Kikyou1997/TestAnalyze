import mysql.connector
import conf
import subprocess
import mysql

import conn_util
import table
import queries


def create_table(sql):
    conn = mysql.connector.connect(
        user=conf.user,
        host=conf.ip,
        db=conf.db_name,
        port=conf.port
    )
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
    finally:
        conn.close()


def import_data():
    for tbl in table.tbl_names:
        cmd = "{} gen --user root --database {} --table {} --rows {}" \
            .format(conf.db_gen_path, conf.db_name, tbl, conf.table_size)
        print(cmd)
        output = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(output)


def check():
    row_count = queries.get_row_count(table.unique_tbl_name)
    assert row_count > conf.table_size * 0.8
    row_count = queries.get_row_count(table.agg_tbl_name)
    assert row_count > conf.table_size * 0.8
    row_count = queries.get_row_count(table.duplicate_tbl_name)
    assert row_count > conf.table_size * 0.8


def drop_db():
    cmd = "echo 'DROP DATABASE IF EXISTS {}' | mysql -h{} -P{} -u{} ".format(conf.db_name, conf.ip, conf.port,
                                                                             conf.user)
    subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def clear_stats():
    conn_util.execute_query("delete from column_statistics where id > 0", db_name=conf.internal_db)
    conn_util.execute_query("delete from histogram_statistics where id > 0", db_name=conf.internal_db)
    conn_util.execute_query("delete from table_statistics where id > 0", db_name=conf.internal_db)


def init_env():
    clear_stats()
    drop_db()
    cmd = "echo 'create database {}' | mysql -h{} -P{} -u{} ".format(conf.db_name, conf.ip, conf.port, conf.user)
    subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    create_table(table.agg_table)
    create_table(table.unique_table)
    create_table(table.duplicate_table)
    import_data()
    check()
