import os
import socket
import time

"""
The delay is 1 second. Therefore we will try for 30 seconds.
"""
MAX_RETRY_COUNT = 30

MYSQL_HOST = os.getenv("DATABASE_HOST", "mysql")
MYSQL_PORT = int(os.getenv("DATABASE_PORT", 3306))


def wait_for_mysql():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    retry_count = 0
    while retry_count < MAX_RETRY_COUNT:
        try:
            s.connect((MYSQL_HOST, MYSQL_PORT))
            s.close()
            break
        except socket.error as ex:
            time.sleep(1)
            retry_count += 1

    # Raise a command error if we still aren't connected.
    if MAX_RETRY_COUNT == retry_count:
        raise Exception(
            f'Unable to connect to database: "{MYSQL_HOST}:{MYSQL_PORT}". '
            f"Make sure it is running."
        )


if __name__ == "__main__":
    wait_for_mysql()
