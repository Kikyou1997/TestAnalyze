from datetime import datetime

import conf
import init
import test
import fileio

# Get current date
current_date = datetime.now()

# Convert date to string
date_string = current_date.strftime("%Y-%m-%d")

if __name__ == '__main__':
    init.init_env()
    fileio.write_to_file(conf.report_output_path,
                         date_string + " table size: "
                         + str(conf.table_size) + " " + "\n" + test.test_sync_analyze() + "\n")
    test.test_preload()
    test.test_drop_expired_job()
    test.test_hist()
    test.test_async_analyze()
    test.test_kill_async_analyze()
    test.test_be_crash()
