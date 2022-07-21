from argparse import ArgumentParser
from asyncio import Queue, create_task, gather, run
from datetime import datetime
from ipaddress import IPv4Network
from logging import StreamHandler, basicConfig, getLogger, info
from os import cpu_count

from icmplib import async_ping


def time():
    return datetime.now().replace(microsecond=0)


def arguments():
    tasks = int(cpu_count() * 2.5)

    parser = ArgumentParser()
    parser.add_argument(
        "range",
        help="network id and subnet bits, e.g. 192.168.1.0/24",
        type=IPv4Network,
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="only print hosts to screen",
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
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        metavar="path",
        help="output to a file",
    )

    args = parser.parse_args()

    return args


async def sweeper(queue: Queue, wait: float, success: list, failed: list):
    while True:
        host = await async_ping(await queue.get(), count=1, timeout=wait)

        if not host.is_alive:
            failed.append(host.address)
        else:
            success.append(host.address)
            info(host.address)

        queue.task_done()


async def main():
    args = arguments()
    queue = Queue()
    tasks = []
    success = []
    failed = []

    basicConfig(
        filename=args.output,
        filemode="w",
        format="%(message)s",
        level=20,  # INFO
    )

    if args.output is not None:
        # Re-enable the logger to logg to the screen if output path is given.
        console = StreamHandler()
        getLogger().addHandler(console)

    if not args.quiet:
        info(
            f"\n> IP Range: {args.range}"
            f"\n> Tasks: {args.tasks}"
            f"\n> Quiet: {args.quiet}"
            f"\n> Wait: {args.wait}s\n",
        )

    # Generate a number of hosts from the given network id and subnet bits.
    for host in args.range.hosts():
        # And append each host to the queue.
        queue.put_nowait(host.exploded)

    start = time()

    for _ in range(args.tasks):
        task = create_task(sweeper(queue, args.wait, success, failed))
        tasks.append(task)

    await queue.join()

    for task in tasks:
        task.cancel()

    await gather(*tasks, return_exceptions=True)
    end = time()

    if not args.quiet:
        info(
            f"\nFinished in: {end - start} | "
            f"Success: {len(success)}, "
            f"Failed: {len(failed)}, "
            f"Total: {len(success) + len(failed)}",
        )


if __name__ == "__main__":
    try:
        run(main())
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
