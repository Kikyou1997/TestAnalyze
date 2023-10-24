import psutil
import time

output_file = "system_stats.txt"


def get_system_stats():
    memory_usage = psutil.virtual_memory()
    cpu_usage = psutil.cpu_percent(interval=1)

    return {
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
        "memory_usage_percent": memory_usage.percent,
        "cpu_usage_percent": cpu_usage
    }


def write_stats_to_file(stats):
    with open(output_file, 'a') as file:
        file.write(f"Timestamp: {stats['timestamp']}\n")
        file.write(f"Memory Usage (%): {stats['memory_usage_percent']}\n")
        file.write(f"CPU Usage (%): {stats['cpu_usage_percent']}\n\n")


if __name__ == "__main__":
    try:
        while True:
            system_stats = get_system_stats()
            write_stats_to_file(system_stats)
            time.sleep(30)
    except KeyboardInterrupt:
        print("Monitoring stopped.")
