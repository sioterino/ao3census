from bs4 import BeautifulSoup, ResultSet

from datetime import datetime, timedelta
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

    @staticmethod
    def int2str(num: int) -> str:
        num_str: str = str(num)[::-1]
        parts = [num_str[i:i+3] for i in range(0, len(num_str), 3)]

        return '.'.join(parts)[::-1]

    @staticmethod
    def seconds_to_time(seconds: int):
        time_units = [
            ("year", 60 * 60 * 24 * 365),
            ("month", 60 * 60 * 24 * 30),
            ("week", 60 * 60 * 24 * 7),
            ("day", 60 * 60 * 24),
            ("hour", 60 * 60),
            ("minute", 60),
            ("second", 1),
        ]

        time_strings = []
        for unit, duration in time_units:
            value = seconds // duration
            seconds %= duration
            if value > 0:
                unit_str = f"{value} {unit}{'s' if value > 1 else ''}"
                time_strings.append(unit_str)

        return " ".join(time_strings)

    @staticmethod
    def order_dict_by_value(dictionary: dict):
        return {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1], reverse=True)}



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


if __name__ == '__main__':
    a = Utils.seconds_to_time(1)
    print(a)