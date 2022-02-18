import datetime
import ipaddress
from concurrent.futures import ThreadPoolExecutor

from pythonping import ping


def scanner(address):
    response = ping(address, count=1, timeout=1)

    if response.success():
        print(address)
    else:
        pass


def convert_range(address_range):

    address_list = []

    for address in ipaddress.IPv4Network(address_range):
        address_list.append(address.exploded)
    return address_list


def current_time():
    return datetime.datetime.now().replace(microsecond=0)


def main():
    start = current_time()
    addresses = convert_range("192.168.55.0/24")

    with ThreadPoolExecutor() as executor:
        executor.map(scanner, addresses)
    end = current_time()
    print(f"\nFinished: {end - start}")


if __name__ == "__main__":
    main()
