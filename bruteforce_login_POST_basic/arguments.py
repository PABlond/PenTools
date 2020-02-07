import argparse


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', help='List file to use', required=True)
    parser.add_argument('--url', '-U', help='Url to bruteforce', required=True)
    parser.add_argument('--avoid', '-a', help='Text to avoid',
                        default='Invalid username')
    parser.add_argument('--check_username', '-cu',
                        help='Check username - [!] True if specified', default=False)
    parser.add_argument('--username_param', '-uu',
                        help='Parameter to use for username', default="username")
    parser.add_argument('--password_param', '-up',
                        help='Parameter to use for username', default="password")
    parser.add_argument('--username', '-u', help='Default username to use',
                        required=False, default="admin")
    parser.add_argument('--password', '-p', help='Default password to use',
                        required=False, default="123456789")
    return parser.parse_args()
