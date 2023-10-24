import time

import conn_util
import fileio
from datetime import datetime


def test_async():
    tbl_name = "dup_huolala_wide_table_100"
    conn_util.execute_query("ANALYZE TABLE {} WITH FULL".format(tbl_name), db_name="zfr_test")
    start = time.time()
    d = datetime.now()
    while True:
        finished = len(conn_util.execute_query("SHOW COLUMN CACHED STATS {}".format(tbl_name), db_name="zfr_test"))
        print("Finished: {}".format(finished))
        if finished < 100:
            time.sleep(10)
            continue
        break
    end = time.time()

    path = "/root/cost_time_DONT_DELETE_THIS_FILE"
    fileio.append_to_file(path, "cost time in secs: {}".format(end - start))
    fileio.append_to_file(path, "start: {} end: {}".format(d, datetime.now()))


if __name__ == '__main__':
    test_async()
