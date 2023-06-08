import json
import time

import conf
import conn_util
import report
import table
import subprocess
import assert_util


def wait_fe_ready():
    waited_time = 0
    while not conn_util.is_port_open(conf.ip, conf.port):
        time.sleep(10)
        waited_time += 10
        if waited_time >= conf.fe_boot_timeout_in_sec:
            raise Exception("FE boot may failed")


def restart_fe():
    subprocess.run(conf.fe_bin_path + "/stop_fe.sh")
    subprocess.run([conf.fe_bin_path + "/start_fe.sh", "--daemon"])
    wait_fe_ready()


def stop_be():
    subprocess.run(conf.be_bin_path + "/stop_be.sh")


def start_be():
    subprocess.run([conf.be_bin_path + "/start_be.sh", "--daemon"])
    time.sleep(conf.be_boot_cost_time_in_sec)


def get_cost_time(func):
    start = time.time()
    func()
    return time.time() - start


def analyze_sync(tbl_name):
    template = "ANALYZE TABLE {} WITH SYNC"
    conn_util.execute_query(template.format(tbl_name))


def verify(tbl_name):
    conn_util.execute_query("SELECT COUNT(*) FROM {}".format(tbl_name))
    rs = conn_util.execute_query("SHOW COLUMN STATS {}".format(tbl_name), fetch=conn_util.fetchall_with_wrapp)
    for r in rs:
        col_name = r["column_name"]
        c = conn_util.execute_query("SELECT MIN({}) AS min,"
                                    "MAX({}) AS max,"
                                    "SUM(CASE WHEN {} IS NULL THEN 1 ELSE 0 END) AS num_null "
                                    "FROM {}".format(col_name, col_name, col_name, tbl_name),
                                    fetch=conn_util.fetch_one_with_wrapp)
        assert int(float(r["num_null"])) == int(c["num_null"])


def test_sync_analyze():
    headers = ["tbl", "cost_time(round 1)", "cost_time(round 2)"]
    rows = []
    for tbl in table.tbl_names:
        cost_time1 = get_cost_time(lambda: (
            analyze_sync(tbl)
        ))
        time.sleep(1)
        verify(tbl)
        cost_time2 = get_cost_time(lambda: (
            analyze_sync(tbl)
        ))
        rows.append([tbl, cost_time1, cost_time2])
    return report.generate_markdown_table(headers, rows)


def test_preload():
    restart_fe()
    time.sleep(conf.fe_precache_load_cost_time_in_sec)
    for tbl in table.tbl_names:
        verify(tbl)


def test_drop_expired_job():
    conn_util.execute_query("DROP TABLE agg_all")
    conn_util.execute_query("DROP EXPIRED STATS")
    r = conn_util.execute_query("SELECT COUNT(*) FROM column_statistics WHERE col_id like 'a%'",
                                db_name=conf.internal_db)
    assert r[0][0] == 0


def test_hist():
    conn_util.execute_query("ANALYZE TABLE duplicate_all WITH SYNC WITH HISTOGRAM WITH BUCKETS 5")
    for i in range(0, 13):
        col_name = "d" + str(i)
        r = conn_util.execute_query("SELECT buckets FROM histogram_statistics WHERE col_id = '{}'".format(col_name),
                                    fetch=conn_util.fetch_one, db_name=conf.internal_db)
        json_struct = json.loads(r[0])
        buckets_array = json_struct["buckets"]
        temp = """
            SELECT SUM(CASE WHEN {} >= '{}' AND {} <= '{}' THEN 1 ELSE 0 END) AS count,
                   SUM(CASE WHEN {} < '{}' THEN 1 ELSE 0 END) AS pre_sum FROM duplicate_all
            """
        for b in buckets_array:
            r = conn_util.execute_query(temp.format(col_name, b["lower"], col_name, b["upper"], col_name, b["lower"]),
                                        fetch=conn_util.fetch_one)
            assert_util.assert_equals(r[0], b["count"], "column name: " + col_name + "'s histogram may have fault")
            assert r[1] == b["pre_sum"]


def test_async_analyze():
    conn_util.execute_query("DELETE FROM column_statistics WHERE id > 0", db_name=conf.internal_db)
    restart_fe()
    job_id = conn_util.execute_query("ANALYZE TABLE duplicate_all", fetch=conn_util.fetch_one_with_wrapp)["Job_Id"]
    cost_time = 0
    while True:
        r = conn_util.execute_query("SHOW ANALYZE " + job_id, fetch=conn_util.fetch_one_with_wrapp)["state"]
        if r == "FINISHED":
            break
        if r == "FAILED":
            raise Exception("Failed to analyze async")
        time.sleep(10)
        cost_time += 10
        if cost_time >= conf.fe_analyze_timeout_in_sec:
            raise Exception("Analyze async timeout")

    verify(table.duplicate_tbl_name)


def test_kill_async_analyze():
    pass
    # job_id = conn_util.execute_query("ANALYZE TABLE duplicate_all", fetch=conn_util.fetch_one_with_wrapp)["Job_Id"]
    # conn_util.execute_query("KILL ANALYZE " + job_id)
    # state = conn_util.execute_query("SHOW ANALYZE " + job_id, fetch=conn_util.fetch_one_with_wrapp)["state"]
    # assert state == "FAILED"


def test_be_crash():
    pass
    # try:
    #     job_id = conn_util.execute_query("ANALYZE TABLE duplicate_all", fetch=conn_util.fetch_one_with_wrapp)["Job_Id"]
    #     stop_be()
    #     state = conn_util.execute_query("SHOW ANALYZE " + job_id, fetch=conn_util.fetch_one_with_wrapp)["state"]
    #     assert state == "FAILED"
    # finally:
    #     start_be()
