import conn_util


def get_row_count(tbl_name: str):
    rs = conn_util.execute_query("SELECT COUNT(*) AS row_count FROM {}".format(tbl_name), fetch=conn_util.fetch_one,
                                 enable_stats_check=False)
    return rs[0]
