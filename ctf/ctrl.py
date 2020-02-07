import requests
import multiprocessing


class BF:
    def __init__(self, file: str, url: str, avoid_text: str,
                 check_username: bool, username: str, password: str,
                 username_param: str, password_param: str):
        self.words_filepath = file
        self.avoid_text = avoid_text
        self.url_login = url
        self.words = []
        self.set_words()
        self.results = []
        self.username = username
        self.password = password
        self.check_username = check_username
        self.username_param = username_param
        self.password_param = password_param

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
        try:
            username, password = self.get_credentials(word=word)

            r = requests.post(self.url_login, data={
                self.username_param: username,
                self.password_param: password
            })

            if not self.avoid_text in r.text:
                print(word)
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
