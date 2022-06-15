from argparse import ArgumentParser
from datetime import datetime
from ipaddress import IPv4Network
from os import cpu_count
from queue import Queue
from threading import Thread

from pythonping import ping


def scan(queue, success, failed):
    while True:
        ip = queue.get()
        response = ping(ip, count=1, timeout=0.2)

        if response.success():
            success.append(ip)
            print(ip)
        else:
            failed.append(ip)

        queue.task_done()


def main():
    queue = Queue()
    parser = ArgumentParser()
    parser.add_argument("IP_RANGE", help="ip range of the network, e.g. 192.168.1.0/24")
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="increase output verbosity",
    )
    args = parser.parse_args()

    success = []
    failed = []
    workers = cpu_count() * 10

    for ip in IPv4Network(args.IP_RANGE).hosts():
        queue.put(ip.exploded)

    start = datetime.now().replace(microsecond=0)

    for _ in range(workers):
        Thread(target=scan, args=(queue, success, failed), daemon=True).start()

    queue.join()

    end = datetime.now().replace(microsecond=0)

    if args.verbose:
        print(
            f"\nFinished in: {end - start} |",
            f"Success: {len(success)} Failed: {len(failed)}",
        )


if __name__ == "__main__":
    main()
