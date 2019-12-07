import argparse
import nmap
import threading


"""
This script allows you to perform (TCP only) scan on a target using nmap. 

usage: scanner.py [-h] [--ip IP] [--range RANGE] [--specific SPECIFIC]
                  [--version] [--xmas]

optional arguments:
  -h, --help           show this help message and exit
  --ip IP              REQUIRED: Who is you target ?
  --range RANGE        OPTIONAL : Range ports to scan
  --specific SPECIFIC  OPTIONAL: Scan specific ports. Eg: 22,80,443
  --version            OPTIONAL: Version detection interrogates ports to
                       determine more about what is actually running
  --xmas               OPTIONAL: Sets the FIN, PSH, and URG flags, lighting
                       the packet up like a Christmas tree.

Eg:
python scanner.py --version --ip 192.168.1.1 --specific 22,80,90 
python scanner.py --ip 192.168.1.1 --range 10000-65535
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
    parser.add_argument("--ip", help="REQUIRED: Who is you target ?")
    parser.add_argument(
        '--range', type=str, help='OPTIONAL : Range ports to scan', default="1-1000", required=False)
    parser.add_argument(
        "--specific", help="OPTIONAL: Scan specific ports. Eg: 22,80,443", default="0", required=False)
    parser.add_argument(
        "--version", help="OPTIONAL: Version detection interrogates ports to determine more about what is actually running", action="store_true")
    parser.add_argument(
        "--xmas", help="OPTIONAL: Sets the FIN, PSH, and URG flags, lighting the packet up like a Christmas tree.", action="store_true")
    args = parser.parse_args()

    arguments_arr = []

    if args.version is True:
        arguments_arr.append("-sV --version-intensity 5 --allports")
    if args.xmas is True:
        arguments_arr.append("-sX")

    arguments = " ".join(arguments_arr)
    print(arguments)
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
