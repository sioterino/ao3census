from bs4 import BeautifulSoup, ResultSet
from requests import Response, Session
from parse import Parse
from time import sleep
from tqdm import tqdm
from pandas import DataFrame
import pandas as pd
import requests
import random
import re
from datetime import datetime

# from InquirerPy import inquirer as iq

all_titles: list = []
all_authors: list = []

df_works: DataFrame = pd.DataFrame(columns=['title', 'authors', 'fandoms', 'rating', 'warnings', 'orientation',
                                            'status', 'update', 'tags', 'language', 'words', 'chapters',
                                            'collections', 'comments', 'kudos', 'bookmarks', 'hits'])


# requests access to a fandom page on ao3
def access_page(fandom: str, category: str, page: int, is_session: bool, session: Session) -> Response:
    # sets default url
    url: str = f'https://archiveofourown.org/tags/{fandom}%20({category})/works?page={page}'
    # sends a request message get to the server
    if is_session:
        print("\nusing session")
        response: Response = session.get(url)
    else:
        print("using request")
        response: Response = requests.get(url)

    # checks status_code of the page and handles possible outcomes
    checks_sc(response.status_code)

    return response


# checks if access was successful
def checks_sc(status_code):
    match status_code:
        case 200:
            print("sc: OK")
        case 404:
            print("sc: not found")
            exit(1)
        case __:
            print(f"unexpected sc: {status_code}")
            exit(1)


# parses pages into html using BeautifulSoup
def get_html_of_page(fandom: str, category: str, is_session: bool, session: Session, page: int = 1) -> BeautifulSoup:
    # trys accessing the page and handles errors
    try:
        response: Response = access_page(
            fandom=fandom,
            category=category,
            page=page,
            is_session=is_session,
            session=session)
    except Exception as e:
        print(f"(get_html_of_page) An error occurred: {e}")
        exit(1)

    return BeautifulSoup(response.content, 'html.parser')


# checks to if the name has any spaces
def fandom_name(name: str) -> str:
    if ' ' in name:
        return name.replace(" ", "%20")
    else:
        return name


# gets the number of pages said fandom page has
def get_number_of_pages(soup: BeautifulSoup) -> int:
    a_tag: ResultSet = soup.find('ol', class_='pagination actions').findAll('a')

    a_text: list = []
    for a in a_tag:
        if not bool(re.search(r'[a-zA-Z]', a.text)):
            a_text.append(int(a.text))

    return a_text[-1]


# parses html into a dataframe
def parse_into_df(soup: BeautifulSoup) -> dict:
    # parses all works into a list
    work_list: list = soup.select('ol.work.index.group li.work.blurb.group')

    global all_titles
    # parses all TITLES from given page into a list
    page_titles: list = Parse.get_titles(work_list)
    # saves all titles from given page into a global list of titles
    for title in page_titles:
        all_titles.append(title)

    global all_authors
    # parses all AUTHORS from given page into a list
    page_authors: list = Parse.get_authors(work_list)
    # saves all authors from given page into a global list of authors
    for author in page_authors:
        all_authors.append(author)

    return {'title': all_titles, 'authors': all_authors}


def save_dataframe(dict_works: dict, fandom: str):
    file_name = f"./results/works_{fandom}_{datetime.now().strftime("%Y%m%d")}.csv"
    global df_works
    df_works = pd.concat([df_works, pd.DataFrame(dict_works)], ignore_index=True)
    df_works.to_csv(file_name, index=False, encoding="utf-8")


# main method
def main():
    fandom: str = fandom_name('le sserafim')
    band: str = 'Band'

    html = get_html_of_page(fandom=fandom, category=band, is_session=False, session=None)
    pages = get_number_of_pages(html)

    session = requests.Session()
    pbar = tqdm((range(1, 2)), dynamic_ncols=True, unit="works", leave=False)
    for page in pbar:
        pbar.set_description(f'Fetching page {page}')
        soup = get_html_of_page(fandom=fandom, category=band, is_session=True, session=session, page=page)
        dict_works: dict = parse_into_df(soup)
        save_dataframe(dict_works, fandom)
        sleep(random.randrange(6, 10))

    session.close()
    print("done")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGracefully exiting...\n\n")
