import arguments
import ctrl

"""
usage: [-h] --file FILE --url URL [--avoid AVOID]
                [--check_username CHECK_USERNAME]
                [--login_username LOGIN_USERNAME] [--password PASSWORD]

optional arguments:
  -h, --help            show this help message and exit
  --file FILE, -f FILE  List file to use
  --url URL, -U URL     Url to bruteforce
  --avoid AVOID, -a AVOID
                        Text to avoid
  --check_username CHECK_USERNAME, -cu CHECK_USERNAME
                        Check username - [!] True if specified
  --login_username LOGIN_USERNAME, -l LOGIN_USERNAME
                        Default username to use
  --password PASSWORD, -p PASSWORD
                        Default password to use
"""


if __name__ == '__main__':
    args = arguments.parse()
    check_username = False if not args.check_username else True

    bf = ctrl.BF(file=args.file, url=args.url, avoid_text=args.avoid,
                 username=args.login_username, password=args.password, check_username=check_username,
                 username_param=args.username_param, password_param=args.password_param)
    print('Bruteforce attack will try {0} alternatives'.format(len(bf.words)))
    bf.run()
    bf.print_results()
