from bs4 import BeautifulSoup, ResultSet

from datetime import datetime
import os
import re


class Utils:
    @staticmethod
    def initialize_fandom_data() -> dict:
        return {
            'title': [], 'authors': [], 'crossovers': [], 'rating': [], 'warnings': [],
            'orientations': [], 'status': [], 'update': [], 'ships': [], 'characters': [],
            'tags': [], 'language': [], 'words': [], 'chapters': [], 'collections': [],
            'comments': [], 'kudos': [], 'bookmarks': [], 'hits': [], 'series': []
        }

    @staticmethod
    def fandom_name(name: str) -> str:
        if ' ' in name:
            return name.replace(" ", "%20")
        else:
            return name

    @staticmethod
    def revert_fandom_name(name: str) -> str:
        if '%20' in name:
            return name.replace("%20", "_")
        else:
            return name

    @staticmethod
    def append_dict(fandom_data: dict, page_data: dict) -> dict:
        for key in page_data:
            for value in page_data[key]:
                fandom_data[key].append(value)
        return fandom_data

    @staticmethod
    def validate_file_extension(file_path: str, reader: str) -> bool:
        _, ext = os.path.splitext(file_path)
        return ext.lower() in reader


class PageUtils:
    @staticmethod
    def get_number_of_pages(soup: BeautifulSoup) -> int:
        a_tag: ResultSet = soup.find('ol', class_='pagination actions').findAll('a')

        a_text: list[int] = []
        for a in a_tag:
            if not bool(re.search(r'[a-zA-Z]', a.text)):
                a_text.append(int(a.text))

        return a_text[-1]

    @staticmethod
    def get_original_fandom_name(soup: BeautifulSoup) -> str:
        return soup.find('h2', class_='heading').find('a', class_='tag').text

    @staticmethod
    def define_url(fandom: str, is_category: bool, category: str, page: int = 1):
        if is_category:
            return f'https://archiveofourown.org/tags/{fandom}%20({category})/works?page={page}'
        else:
            return f'https://archiveofourown.org/tags/{fandom}/works?page={page}'


class DfUtils:
    @staticmethod
    def file_name(fandom: str) -> str:
        return f"{DfUtils.result_dir()}works_{Utils.revert_fandom_name(fandom)}_{datetime.now().strftime('%Y%m%d')}.csv"

    @staticmethod
    def result_dir() -> str:
        return f'{os.getcwd()}{'/' if os.name == 'posix' else '\\'}results{'/' if os.name == 'posix' else '\\'}'
