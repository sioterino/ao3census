import pandas as pd
from bs4 import BeautifulSoup
import requests
from requests import Session
import pandas
from pandas import DataFrame
from tqdm import tqdm

from time import sleep
import random

from interface import Interface
from scrape import Login
from scrape import GetPage
from scrape import Dataframe
from utils import Utils, PageUtils, DfUtils

debug: bool = False

login_limit: int = 2

user_data: dict = dict.fromkeys(['login', 'username', 'password', 'fandom', 'is_category', 'category', 'scrape', 'file_path'])

df_works: DataFrame = pandas.DataFrame(columns=list(Utils.initialize_fandom_data().keys()))


def debugging():
    global user_data
    user_data['login'] = True
    user_data['username'] = ''
    user_data['password'] = ''
    user_data['fandom'] = Utils.fandom_name('')
    user_data['is_category'] = True
    user_data['category'] = 'Band'
    user_data['scrape'] = False
    user_data['file_path'] = ''  # .csv


def scrape_ao3():
    session: Session = requests.Session()
    user_data['login'] and Login.try_logging_in(session, user_data['username'], user_data['password'], login_limit)

    url: str = PageUtils.define_url(user_data['fandom'], user_data['is_category'], user_data['category'])
    print(f"Fetching works from url: {url}")
    soup_html: BeautifulSoup = GetPage.get_html_of_page(session=session, url=url)
    pages_number: int = PageUtils.get_number_of_pages(soup_html)
    print(pages_number)

    original_fandom_tag: str = PageUtils.get_original_fandom_name(soup_html)
    fandom_data: dict = Utils.initialize_fandom_data()

    pbar1 = tqdm(range(1, pages_number + 1 if not debug else 4), dynamic_ncols=True, unit="works", leave=True, colour="green")
    for page in pbar1:
        pbar1.set_description(f'Fetching page {page}')
        page_url: str = PageUtils.define_url(user_data['fandom'], user_data['is_category'], user_data['category'], page)

        try:
            soup: BeautifulSoup = GetPage.get_html_of_page(session=session, url=page_url)
        except Exception:
            pbar2 = tqdm(range(1, 61), dynamic_ncols=True, unit="lines", leave=False, colour="red", desc='Fixing errors')
            for _ in pbar2:
                sleep(1)
            session = requests.Session()
            user_data['login'] and Login.try_logging_in(session, user_data['username'], user_data['password'], login_limit)
            soup: BeautifulSoup = GetPage.get_html_of_page(session=session, url=page_url)

        page_data: dict = Dataframe.get_data2df(soup, original_fandom_tag)
        fandom_data = Utils.append_dict(fandom_data, page_data)
        sleep(random.randrange(6, 10))

    user_data['file_path']: str = DfUtils.file_name(user_data['fandom'])
    Dataframe.save_dataframe(page_data=fandom_data, file_name=user_data['file_path'], df_works=df_works)
    session.close()
    print("\n\n\ndone")


if __name__ == '__main__':
    try:
        debug and print('DEBUG MODE')
        debug and debugging()
        # gets user data on how to proceed with the program
        debug or Interface.scanner(user_data)
        # scrapes ao3 website accordingly with user_data
        user_data['scrape'] and scrape_ao3()
        # loads in works dataframe
        user_data['scrape'] or print(f'reading from {user_data['file_path']}')
        df_works = pd.read_csv(user_data['file_path'])

    except KeyboardInterrupt:
        print("\n\nGracefully exiting...\n\n")
