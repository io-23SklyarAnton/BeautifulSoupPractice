import os
from pprint import pprint
from typing import List

from requests import Session
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from requests.compat import urljoin


class ParseShop:
    def __init__(self):
        self.__session = Session()
        self.__user = UserAgent()
        self.__headers = {'user-agent': self.__user.chrome}

    @staticmethod
    def __walk_through_pages(start_page: int, end_page: int):
        for idx in range(start_page, end_page + 1):
            yield f"https://scrapingclub.com/exercise/list_basic/?page={idx}"

    def __get_soup(self, url: str) -> BeautifulSoup:
        response = self.__session.get(url, headers=self.__headers)
        return BeautifulSoup(response.text, 'lxml')

    def __get_description_from_cloth_page(self, url: str):
        soup = self.__get_soup(url)
        description = soup.find("p", class_="card-description")
        return description.text

    def get_all_descriptions(self) -> List[str]:
        result = []
        for url in self.__walk_through_pages(1, 6):
            soup = self.__get_soup(url)
            for cloth_card in soup.find_all("div", class_="w-full rounded border"):
                rel_cloth_url = cloth_card.find("a").get("href")
                abs_cloth_url = urljoin("https://scrapingclub.com", rel_cloth_url)
                description = self.__get_description_from_cloth_page(abs_cloth_url)
                result.append(description)
        return result

    def get_all_cloth_names(self) -> List[str]:
        result = []
        for url in self.__walk_through_pages(1, 6):
            soup = self.__get_soup(url)
            for cloth_card in soup.find_all("div", class_="w-full rounded border"):
                cloth_name = cloth_card.find("h4").text.replace("\n", "")
                result.append(cloth_name)
        return result

    def get_all_images_url(self) -> List[str]:
        result = []
        for url in self.__walk_through_pages(1, 6):
            soup = self.__get_soup(url)
            rel_paths = soup.find_all("img", class_='card-img-top img-fluid')
            result.extend(list(map(lambda x: urljoin("https://scrapingclub.com", x.get("src")), rel_paths)))
        return result


def main():
    parse_shop = ParseShop()
    pprint(parse_shop.get_all_descriptions())
    pprint(parse_shop.get_all_cloth_names())
    pprint(parse_shop.get_all_images_url())


if __name__ == '__main__':
    main()
