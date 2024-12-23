from bs4 import BeautifulSoup
import numpy
import pandas
import pandas as pd
from pandas import DataFrame
import requests
from requests import Session
from tqdm import tqdm

import os
import random
from time import sleep

from interface import Interface
from read import Basics, Ordered
from scrape import Login, GetPage, Dataframe
from utils import Utils, PageUtils, DfUtils

debug: bool = True

login_limit: int = 2

user_data: dict = dict.fromkeys(['login', 'username', 'password', 'fandom', 'is_category', 'category', 'scrape', 'file_path'])

df_works: DataFrame = pandas.DataFrame(columns=list(Utils.initialize_fandom_data().keys()))


def debugging():
    global user_data
    user_data['scrape'] = False
    user_data['file_path'] = 'E:\\ao3census\\results\\works_le_sserafim_20241215.csv'  # .csv

    user_data['login'] = True
    user_data['username'] = ''
    user_data['password'] = ''

    user_data['fandom'] = Utils.fandom_name('')
    user_data['is_category'] = True
    user_data['category'] = 'Band'


def scrape_ao3():
    if not os.path.exists(DfUtils.result_dir()):
        os.makedirs(DfUtils.result_dir())

    session: Session = requests.Session()
    user_data['login'] and Login.try_logging_in(session, user_data['username'], user_data['password'], login_limit)

    url: str = PageUtils.define_url(user_data['fandom'], user_data['is_category'], user_data['category'])
    print(f"Fetching works from url: {url}")
    soup_html: BeautifulSoup = GetPage.get_html_of_page(session=session, url=url)
    pages_number: int = PageUtils.get_number_of_pages(soup_html)
    print(f'fandom pages: {pages_number}')

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
    print("\ndone")


def print_data(work_data: dict):
    for key in work_data:
        if isinstance(work_data[key], (int, numpy.int_)):
            print(f'{key}: {Utils.int2str(work_data[key])}')
        else:
            print(f'{key}: {work_data[key]}')


def data_analysis(df: DataFrame):
    work_data: dict = {}

    work_data['total_works']: int = Basics.number_of_works(df)

    work_data['total_words'] = Basics.get_totals(df, 'words')
    work_data['avg_work'] = work_data['total_words'] / work_data['total_works']
    work_data['238_word/s'] = {work_data['total_words'] / 238}
    work_data['how_long'] = Utils.seconds_to_time(work_data['total_words'])

    work_data['lowercased_titles'] = len(Basics.get_lowercases(df))
    work_data['orphaned'] = Basics.get_orphans(df)['orphaned']
    work_data['anonymous'] = Basics.get_orphans(df)['anonymous']

    work_data['total_chapters'] = Basics.get_totals(df, 'chapters')
    work_data['avg_chapters'] = work_data['total_chapters'] / work_data['total_works']

    work_data['total_comments'] = Basics.get_totals(df, 'comments')
    work_data['avg_comments'] = work_data['total_comments'] / work_data['total_works']

    work_data['total_kudos'] = Basics.get_totals(df, 'kudos')
    work_data['avg_kudos'] = work_data['total_kudos'] / work_data['total_works']

    work_data['total_bookmarks'] = Basics.get_totals(df, 'bookmarks')
    work_data['avg_bookmarks'] = work_data['total_bookmarks'] / work_data['total_works']

    work_data['total_hits'] = Basics.get_totals(df, 'hits')
    work_data['avg_hits'] = work_data['total_hits'] / work_data['total_works']

    work_data['total_collections'] = Basics.get_totals(df, 'collections')
    work_data['avg_collections'] = work_data['total_collections'] / work_data['total_works']

    work_data['language'] = Ordered.most_of(df, 'language')
    work_data['tags'] = Ordered.most_of(df, 'tags')
    work_data['avg_tags'] = len(work_data['tags']) / work_data['total_works']
    work_data['characters'] = Ordered.most_of(df, 'characters')
    work_data['ships'] = Ordered.most_of(df, 'ships')
    work_data['status'] = Ordered.most_of(df, 'status')
    work_data['orientations'] = Ordered.most_of(df, 'orientations')
    work_data['warnings'] = Ordered.most_of(df, 'warnings')
    work_data['rating'] = Ordered.most_of(df, 'rating')
    work_data['crossovers'] = Ordered.most_of(df, 'crossovers')
    work_data['authors'] = Ordered.most_of(df, 'authors')

if __name__ == '__main__':
    try:
        # debug and print('DEBUG MODE')
        debug and debugging()
        # gets user data on how to proceed with the program
        debug or Interface.scanner(user_data)
        # scrapes ao3 website accordingly with user_data
        user_data['scrape'] and scrape_ao3()
        # loads in works dataframe
        # user_data['scrape'] or print(f'reading from {user_data['file_path']}')
        df_works = pd.read_csv(user_data['file_path'])
        data_analysis(df_works)

    except KeyboardInterrupt:
        print("\nGracefully exiting...\n")
