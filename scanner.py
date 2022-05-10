from argparse import ArgumentParser
from datetime import datetime
from ipaddress import IPv4Network
from threading import Thread

from pythonping import ping


def scan(ip, success, failed):

    response = ping(ip, count=1, timeout=2)

    if response.success():
        success.append(ip)
    else:
        failed.append(ip)


def main():
    parser = ArgumentParser()
    parser.add_argument("IP_RANGE", help="IP Range of the network, e.g. 192.168.1.0/24")
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="increase output verbosity",
    )

    args = parser.parse_args()

    threads = []
    success = []
    failed = []

    start = datetime.now().replace(microsecond=0)

    for ip in IPv4Network(args.IP_RANGE).hosts():
        threads.append(Thread(target=scan, args=(ip.exploded, success, failed)))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    end = datetime.now().replace(microsecond=0)

    if args.verbose:
        print("\n".join(success))
        print(
            f"\nFinished in: {end - start} |",
            f"Success: {len(success)} Failed: {len(failed)}",
        )
    else:
        print("\n".join(success))


if __name__ == "__main__":
    main()
