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


class PingSweeper():
    
    def __init__(self):
        self.tasks = []
        self.success = 0
        self.failed = 0
        self.args = arguments()
        self.queue = Queue()
        
        basicConfig(
            filename=self.args.output,
            filemode="w",
            format="%(message)s",
            level=20,  # INFO
        )
        
        if self.args.output is not None:
            # Re-enable the logger to logg to the screen if output path is given.
            getLogger().addHandler(StreamHandler())

    async def sweeper(self, queue: Queue, wait: float):
        while True:
            host = await async_ping(await queue.get(), count=1, timeout=wait)

            if not host.is_alive:
                self.failed += 1
            else:
                self.success += 1
                info(host.address)

            queue.task_done()

    async def run(self):
        if not self.args.quiet:
            info(
                f"\n> IP Range: {self.args.range}"
                f"\n> Tasks: {self.args.tasks}"
                f"\n> Quiet: {self.args.quiet}"
                f"\n> Wait: {self.args.wait}s\n",
            )

        # Generate a number of hosts from the given network id and subnet bits.
        for host in self.args.range.hosts():
            # And append each host to the queue.
            self.queue.put_nowait(host.exploded)

        start = time()
        for _ in range(self.args.tasks):
            task = create_task(self.sweeper(self.queue, self.args.wait))
            self.tasks.append(task)

        await self.queue.join()

        for task in self.tasks:
            task.cancel()

        await gather(*self.tasks, return_exceptions=True)
        end = time()

        if not self.args.quiet:
            info(
                f"\nFinished in: {end - start} | "
                f"Success: {self.success}, "
                f"Failed: {self.failed}, "
                f"Total: {self.success + self.failed}",
            )

async def main():
    pingSweeper = PingSweeper()
    await pingSweeper.run()


if __name__ == "__main__":
    try:
        run(main())
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
