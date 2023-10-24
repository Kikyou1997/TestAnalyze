import sys
import time


import conn_util


def test_sample(sr: bool):
    times = 0
    cost_times = []
    while times < 20:
        conn_util.execute_query("DROP STATS dup_huolala_wide_table_100", db_name="zfr_test")
        start = time.time()
        if sr:
            conn_util.execute_query("ANALYZE SAMPLE TABLE zfr_test.dup_huolala_wide_table_100 "
                                    "PROPERTIES ('statistic_sample_collect_rows' = '10000000'); ",
                                    db_name="zfr_test")
        else:
            conn_util.execute_query("ANALYZE TABLE dup_huolala_wide_table_100 WITH SAMPLE ROWS 10000000",
                                    db_name="zfr_test")
            while True:
                finished = len(conn_util.execute_query("SHOW COLUMN CACHED STATS dup_huolala_wide_table_100", db_name="zfr_test"))
                print("Finished: {}".format(finished))
                if finished < 100:
                    time.sleep(1)
                    continue
                break
        end = time.time()
        cost_times.append(end - start)
        times += 1
    print("avg time: {}".format(sum(cost_times) / len(cost_times)))


if __name__ == '__main__':
    args = sys.argv
    test_sample(args[1] == "s")
