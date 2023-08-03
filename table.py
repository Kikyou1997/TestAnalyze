import conf

unique_tbl_name = "unique_all"
duplicate_tbl_name = "duplicate_all"
agg_tbl_name = "agg_all"
incremental_analyze_test_tbl_name = "t1"

tbl_names = [unique_tbl_name, duplicate_tbl_name, agg_tbl_name]

unique_table = """
            CREATE TABLE IF NOT EXISTS `unique_all` (
            `u3` int(11) null comment "",
            `u0` boolean null comment "",
            `u1` tinyint(4) null comment "",
            `u2` smallint(6) null comment "",
            `u4` bigint(20) null comment "",
            `u5` decimalv3(9, 3) null comment "",
            `u6` char(36) null comment "",
            `u10` date null comment "",
            `u11` datetime null comment "",
            `u7` varchar(64) null comment "",
            `u8` double null comment "",
            `u9` float null comment "",
            `u12` string  null comment "",
            `u13` largeint(40)  null comment ""
        ) engine=olap
        UNIQUE KEY(`u3`)
        DISTRIBUTED BY HASH(`u3`) BUCKETS 5 properties("replication_num" = "1")
"""

duplicate_table = """
        CREATE TABLE IF NOT EXISTS `duplicate_all` (
            `d3` int(11) null comment "",
            `d0` boolean null comment "",
            `d1` tinyint(4) null comment "",
            `d2` smallint(6) null comment "",
            `d4` bigint(20) null comment "",
            `d5` decimalv3(9, 3) null comment "",
            `d6` char(36) null comment "",
            `d10` date null comment "",
            `d11` datetime null comment "",
            `d7` varchar(64) null comment "",
            `d8` double null comment "",
            `d9` float null comment "",
            `d12` string  null comment "",
            `d13` largeint(40)  null comment ""
        ) engine=olap
        DUPLICATE KEY(`d3`)
        DISTRIBUTED BY HASH(`d3`) BUCKETS 5 properties("replication_num" = "1")
"""

agg_table = """
        CREATE TABLE IF NOT EXISTS `agg_all` (
            `a0` boolean null comment "",
            `a1` tinyint(4) null comment "",
            `a2` smallint(6) null comment "",
            `a3` int(11) null comment "",
            `a4` bigint(20) null comment "",
            `a5` decimalv3(9, 3) null comment "",
            `a6` char(36) null comment "",
            `a10` date null comment "",
            `a11` datetime null comment "",
            `a7` varchar(64) null comment "",
            `a8` double max null comment "",
            `a9` float sum null comment "",
            `a12` string replace null comment "",
            `a13` largeint(40) replace null comment ""
        ) engine=olap
        DISTRIBUTED BY HASH(`a1`) BUCKETS 5 properties("replication_num" = "1")
"""

incremental_analyze_test_tbl = """
    CREATE TABLE t1 (col1 varchar(11451) not null, col2 int not null, col3 int not null)
    DUPLICATE KEY(col1)
    DISTRIBUTED BY HASH(col1)
    BUCKETS 3
    PROPERTIES(
        "replication_num"="1"
    );
"""
