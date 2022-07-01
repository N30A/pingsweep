from argparse import ArgumentParser
from asyncio import Queue, create_task, gather, run
from datetime import datetime
from ipaddress import IPv4Network
from os import cpu_count

from icmplib import async_ping


def time():
    return datetime.now().replace(microsecond=0)


def arguments():
    tasks = int(cpu_count() * 2.5)

    parser = ArgumentParser()
    parser.add_argument(
        "ip_range",
        help="ip range of the network, e.g. 192.168.1.0/24",
        type=IPv4Network,
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="quiet output, only print ip-addresses to screen",
    )
    parser.add_argument(
        "-w",
        "--wait",
        type=float,
        metavar="sec",
        default=1,
        help="timeout in seconds to wait for each reply (default: 1s)",
    )
    parser.add_argument(
        "-t",
        "--tasks",
        type=int,
        metavar="num",
        default=tasks,
        help=f"number of concurrent tasks (default: {tasks})",
    )

    args = parser.parse_args()

    return args


async def sweeper(
    queue: Queue[str], wait: float, success: list[str], failed: list[str]
):
    while True:
        address = await queue.get()
        host = await async_ping(address, count=1, timeout=wait)

        if not host.is_alive:
            failed.append(host.address)
        else:
            success.append(host.address)
            print(host.address)

        queue.task_done()


async def main():
    success = []
    failed = []
    args = arguments()
    queue = Queue()

    if not args.quiet:
        print(
            f"\n> IP Range: {args.ip_range}",
            f"\n> Tasks: {args.tasks}",
            f"\n> Quiet: {args.quiet}",
            f"\n> Wait: {args.wait}s\n",
        )

    for address in args.ip_range.hosts():
        queue.put_nowait(address.exploded)

    start = time()
    tasks = []
    for _ in range(args.tasks):
        task = create_task(sweeper(queue, args.wait, success, failed))
        tasks.append(task)

    await queue.join()

    for task in tasks:
        task.cancel()

    await gather(*tasks, return_exceptions=True)
    end = time()

    if not args.quiet:
        print(
            f"\nFinished in: {end - start} |",
            f"Success: {len(success)}, Failed: {len(failed)}, Total: {len(success) + len(failed)}",
        )


if __name__ == "__main__":
    try:
        run(main())
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
