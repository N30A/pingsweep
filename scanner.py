from argparse import ArgumentParser
from datetime import datetime
from ipaddress import IPv4Network
from os import cpu_count
from queue import Queue
from threading import Thread

from pythonping import ping


def scan(queue: Queue, wait: float, success: list, failed: list) -> None:
    while True:
        address = queue.get()
        response = ping(address, count=1, timeout=wait)

        if response.success():
            success.append(address)
            print(address)
        else:
            failed.append(address)

        queue.task_done()


def main():
    threads = cpu_count()
    success = []
    failed = []

    queue = Queue()
    parser = ArgumentParser()
    parser.add_argument("ip_range", help="ip range of the network, e.g. 192.168.1.0/24")
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="quiet output, only print ip-addresses to the screen",
    )
    parser.add_argument(
        "-w",
        "--wait",
        type=float,
        metavar="sec",
        default=0.1,
        help="timeout in seconds to wait for each reply (default: 0.1s)",
    )
    parser.add_argument(
        "-t",
        "--threads",
        type=int,
        metavar="int",
        default=threads,
        help=f"number of concurrent threads (default: {threads})",
    )
    args = parser.parse_args()

    if not args.quiet:
        print(
            f"\n> IP Range: {args.ip_range}",
            f"\n> Threads: {args.threads}",
            f"\n> Quiet: {args.quiet}",
            f"\n> Wait: {args.wait}s\n",
        )

    # Append every valid address to the queue from the user specified ip range.
    for address in IPv4Network(args.ip_range).hosts():
        queue.put(address.exploded)

    # Time snapshot
    start = datetime.now().replace(microsecond=0)

    # Start the "scan" function with the amount of threads specified.
    for _ in range(args.threads):
        Thread(
            target=scan,
            args=(queue, args.wait, success, failed),
            daemon=True,
        ).start()

    # Wait until all work is finished before continuing.
    queue.join()

    # Time snapshot
    end = datetime.now().replace(microsecond=0)

    if not args.quiet:
        print(
            f"\nFinished in: {end - start} |",
            f"Success: {len(success)}, Failed: {len(failed)}, Total: {len(success) + len(failed)}",
        )


if __name__ == "__main__":
    main()
