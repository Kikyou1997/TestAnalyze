import concurrent.futures
from datetime import datetime
import subprocess
import time

# Define the commands to execute
commands = ["mysql -h172.21.0.106 -P 19030 -uroot internal_schema < /root/analyze_sql_1",
            "mysql -h172.21.0.106 -P 19030 -uroot internal_schema < /root/analyze_sql_2",
            "mysql -h172.21.0.106 -P 19030 -uroot internal_schema < /root/analyze_sql_3"]


def execute_command(command):
    try:
        completed_process = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE, check=True)
        output = completed_process.stdout
        error_output = completed_process.stderr

        if output:
            print(f"Command output for '{command}':")
            print(output)

        if error_output:
            print(f"Command error output for '{command}':")
            print(error_output)
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with return code {e.returncode}")


if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        start = time.time()
        d = datetime.now()
        # Submit and execute the tasks
        futures = [executor.submit(execute_command, command) for command in commands]

        # Wait for all tasks to complete
        concurrent.futures.wait(futures)
        end = time.time()
        print("cost time in secs: {}".format(end - start))
        print("start: {} end: {}".format(d, datetime.now()))
    # At this point, all tasks have completed
    print("All commands have finished.")
