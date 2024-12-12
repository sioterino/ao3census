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

all_titles: list[str] = []
all_authors: list[str] = []
all_fandoms: list[str] = []

all_ratings: list[str] = []
all_warnings: list[str] = []
all_orientations: list[str] = []
all_status: list[str] = []

all_updates: list = []

all_ships: list[str] = []
all_chars: list[str] = []
all_tags: list[str] = []

all_languages: list[str] = []
all_words: list[int] = []
all_chapters: list[int] = []
all_collections: list[int] = []
all_comments: list[int] = []
all_kudos: list[int] = []
all_bookmarks: list[int] = []
all_hits: list[int] = []

all_series: list[str] = []

df_works: DataFrame = pd.DataFrame(columns=['title', 'authors', 'crossovers', 'rating', 'warnings',
                                            'orientations', 'status', 'update', 'ships', 'characters',
                                            'tags', 'language', 'words', 'chapters', 'collections',
                                            'comments', 'kudos', 'bookmarks', 'hits', 'series'])


# requests access to a fandom page on ao3
def access_page(fandom: str, category: str, page: int, is_session: bool, session: Session) -> Response:
    # sets default url
    url: str = f'https://archiveofourown.org/tags/{fandom}%20({category})/works?page={page}'
    # sends a request message get to the server
    if is_session:
        # print("\nusing session")
        response: Response = session.get(url)
    else:
        # print("using request")
        response: Response = requests.get(url)

    # checks status_code of the page and handles possible outcomes
    checks_sc(response.status_code)

    return response


# checks if access was successful
def checks_sc(status_code):
    match status_code:
        case 200:
            # print("sc: OK")
            pass
        case 404:
            # print("sc: not found")
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


def revert_fandom_name(name: str) -> str:
    if '%20' in name:
        return name.replace("%20", "_")
    else:
        return name


# gets the number of pages said fandom page has
def get_number_of_pages(soup: BeautifulSoup) -> int:
    a_tag: ResultSet = soup.find('ol', class_='pagination actions').findAll('a')

    a_text: list[int] = []
    for a in a_tag:
        if not bool(re.search(r'[a-zA-Z]', a.text)):
            a_text.append(int(a.text))

    return a_text[-1]


def get_original_fandom_name(soup: BeautifulSoup) -> str:
    return soup.find('h2', class_='heading').find('a', class_='tag').text


# parses html into a dataframe
def parse_into_df(soup: BeautifulSoup, fandom_name: str) -> dict:

    work_list: list = soup.select('ol.work.index.group li.work.blurb.group')

    global all_titles
    page_titles: list[str] = Parse.get_titles(work_list)
    for title in page_titles:
        all_titles.append(title)

    global all_authors
    page_authors: list[str] = Parse.get_authors(work_list)
    for author in page_authors:
        all_authors.append(author)

    global all_fandoms
    page_fandoms: list[str] = Parse.get_fandoms(work_list, fandom_name)
    for fandom in page_fandoms:
        all_fandoms.append(fandom)

    global all_ratings
    page_ratings: list[str] = Parse.get_ratings(work_list)
    for rating in page_ratings:
        all_ratings.append(rating)

    global all_warnings
    page_warnings: list[str] = Parse.get_warnings(work_list)
    for warning in page_warnings:
        all_warnings.append(warning)

    global all_orientations
    page_orientations: list[str] = Parse.get_orientations(work_list)
    for orientation in page_orientations:
        all_orientations.append(orientation)

    global all_status
    page_status: list[str] = Parse.get_status(work_list)
    for stat in page_status:
        all_status.append(stat)

    global all_updates
    page_updates: list = Parse.get_updates(work_list)
    for update in page_updates:
        all_updates.append(update)

    global all_ships
    page_ships: list[str] = Parse.get_ships(work_list)
    for ship in page_ships:
        all_ships.append(ship)

    global all_chars
    page_chars: list[str] = Parse.get_chars(work_list)
    for char in page_chars:
        all_chars.append(char)

    global all_tags
    page_tags: list[str] = Parse.get_freeform_tags(work_list)
    for tag in page_tags:
        all_tags.append(tag)

    global all_languages
    page_languages: list[str] = Parse.get_language(work_list)
    for lang in page_languages:
        all_languages.append(lang)

    global all_words
    page_words: list[int] = Parse.get_words(work_list)
    for words in page_words:
        all_words.append(words)

    global all_chapters
    page_chapters: list[int] = Parse.get_chapters(work_list)
    for chaps in page_chapters:
        all_chapters.append(chaps)

    global all_collections
    page_collections: list[int] = Parse.get_collections(work_list)
    for collect in page_collections:
        all_collections.append(collect)

    global all_comments
    page_comments: list[int] = Parse.get_comments(work_list)
    for comments in page_comments:
        all_comments.append(comments)

    global all_kudos
    page_kudos: list[int] = Parse.get_kudos(work_list)
    for kud in page_kudos:
        all_kudos.append(kud)

    global all_bookmarks
    page_bookmarks: list[int] = Parse.get_bookmarks(work_list)
    for marks in page_bookmarks:
        all_bookmarks.append(marks)

    global all_hits
    page_hits: list[int] = Parse.get_hits(work_list)
    for hit in page_hits:
        all_hits.append(hit)

    global all_series
    page_series: list[str] = Parse.get_series(work_list)
    for part in page_series:
        all_series.append(part)

    return {'title': all_titles, 'authors': all_authors, 'crossovers': all_fandoms, 'rating': all_ratings,
            'warnings': all_warnings, 'orientations': all_orientations, 'status': all_status, 'update': all_updates,
            'ships': all_ships, 'characters': all_chars, 'tags': all_tags, 'language': all_languages,
            'words': all_words, 'chapters': all_chapters, 'collections': all_collections, 'comments': all_comments,
            'kudos': all_kudos, 'bookmarks': all_bookmarks, 'hits': all_hits, 'series': all_series}


def save_dataframe(dict_works: dict, fandom: str):
    file_name: str = f"./results/works_{revert_fandom_name(fandom)}_{datetime.now().strftime('%Y%m%d')}.csv"
    global df_works
    df_works = pd.concat([df_works, pd.DataFrame(dict_works)], ignore_index=True)
    df_works.to_csv(file_name, index=False, encoding="utf-8")


# main method
def main():
    fandom: str = fandom_name('le sserafim')
    band: str = 'Band'

    html: BeautifulSoup = get_html_of_page(fandom=fandom, category=band, is_session=False, session=None)
    pages: int = get_number_of_pages(html)
    original_fandom_tag: str = get_original_fandom_name(html)

    session: Session = requests.Session()
    pbar: tqdm = tqdm((range(1, pages - 1)), dynamic_ncols=True, unit="works", leave=False)
    for page in pbar:
        pbar.set_description(f'Fetching page {page}')
        soup: BeautifulSoup = get_html_of_page(fandom=fandom, category=band, is_session=True, session=session, page=page)
        dict_works: dict = parse_into_df(soup, original_fandom_tag)
        save_dataframe(dict_works, fandom)
        sleep(random.randrange(6, 10))

    session.close()
    print("\n\n\ndone")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGracefully exiting...\n\n")
