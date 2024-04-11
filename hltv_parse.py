from requests import Session
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


class Hltv:
    def __init__(self):
        self.__session = Session()
        self.__user = UserAgent()
        self.__headers = {'user-agent': self.__user.chrome}

    def __get_soup(self, url: str) -> BeautifulSoup:
        response = self.__session.get(url, headers=self.__headers)
        return BeautifulSoup(response.text, 'lxml')

    def get_five_upcoming_matches(self):
        soup = self.__get_soup('https://www.hltv.org/matches')

    def get_five_recent_results(self):
        soup = self.__get_soup('https://www.hltv.org/results')

    def get_five_recent_news(self):
        soup = self.__get_soup('https://www.hltv.org')

    def get_big_news(self):
        soup = self.__get_soup('https://www.hltv.org')


def main():
    hltv = Hltv()

    hltv.get_big_news()
    hltv.get_five_recent_news()
    hltv.get_five_upcoming_matches()
    hltv.get_five_recent_results()


if __name__ == '__main__':
    main()
