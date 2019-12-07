import argparse
import nmap
import threading


"""
This script allows you to perform scan on a target using nmap. 

usage: scanner.py [-h] [--range RANGE] [--specific SPECIFIC] [--version]
                  [--ip IP]

optional arguments:
  -h, --help           show this help message and exit
  --range RANGE        Indicates port to scan
  --specific SPECIFIC  Scan specific ports. Eg: 22,80,443
  --version            Activate version scan
  --ip IP              Indicates ip to scan

Eg:
python scanner.py --version --ip 192.168.1.1 --specific 22,80,90 
python scanner.py --ip 192.168.1.1 --range 10000-35000
"""


def nmapScan(ip, port, arguments, lock):
    with lock:
        nm = nmap.PortScanner()
        nm.scan(ip, str(port), arguments=arguments)
        state = nm[ip]['tcp'][port]['state']
        if state == "open":
            port_service = nm[ip]['tcp'][port]['name']
            port_product = nm[ip]['tcp'][port]['product']
            print('[+] tcp/{0} {1} {2} {3}'.format(port,
                                                   state, port_service, port_product))


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--range', type=str, help='Indicates port to scan', default="1-1000", required=False)
    parser.add_argument(
        "--specific", help="Scan specific ports. Eg: 22,80,443", default="0", required=False)
    parser.add_argument(
        "--version", help="Activate version scan", action="store_true")
    parser.add_argument("--ip", help="Indicates ip to scan")
    args = parser.parse_args()
    arguments_arr = []
    if args.version is True:
        arguments_arr.append("-sV")
    arguments = " ".join(arguments_arr)

    ports_range = list(
        range(int(args.range.split('-')[0]), int(args.range.split('-')[1])))

    if args.specific != "0":
        ports_range = [int(x) for x in args.specific.split(',')]

    return args.ip, ports_range, arguments


def main():
    ip, ports_range, arguments = get_args()

    lock = threading.Lock()
    for port in ports_range:
        t = threading.Thread(target=nmapScan, args=(ip, port, arguments, lock))
        t.start()


if __name__ == '__main__':
    main()
