from pandas import DataFrame
import pandas as pd

from .parse import Parse
from utils import *


class Dataframe:
    @staticmethod
    def save_dataframe(page_data: dict, file_name: str, df_works: DataFrame):
        df_works = pd.concat([df_works, pd.DataFrame(page_data)], ignore_index=True)
        df_works.to_csv(file_name, index=False, encoding="utf-8")

    @staticmethod
    def get_data2df(soup: BeautifulSoup, fandom: str) -> dict:

        page_data: dict = Utils.initialize_fandom_data()

        work_list: list = soup.select('ol.work.index.group li.work.blurb.group')

        page_titles: list[str] = Parse.get_titles(work_list)
        for title in page_titles:
            page_data['title'].append(title)

        page_authors: list[str] = Parse.get_authors(work_list)
        for author in page_authors:
            page_data['authors'].append(author)

        page_fandoms: list[str] = Parse.get_fandoms(work_list, fandom)
        for fandom in page_fandoms:
            page_data['crossovers'].append(fandom)

        page_ratings: list[str] = Parse.get_ratings(work_list)
        for rating in page_ratings:
            page_data['rating'].append(rating)

        page_warnings: list[str] = Parse.get_warnings(work_list)
        for warning in page_warnings:
            page_data['warnings'].append(warning)

        page_orientations: list[str] = Parse.get_orientations(work_list)
        for orientation in page_orientations:
            page_data['orientations'].append(orientation)

        page_status: list[str] = Parse.get_status(work_list)
        for stat in page_status:
            page_data['status'].append(stat)

        page_updates: list = Parse.get_updates(work_list)
        for update in page_updates:
            page_data['update'].append(update)

        page_ships: list[str] = Parse.get_ships(work_list)
        for ship in page_ships:
            page_data['ships'].append(ship)

        page_chars: list[str] = Parse.get_chars(work_list)
        for char in page_chars:
            page_data['characters'].append(char)

        page_tags: list[str] = Parse.get_freeform_tags(work_list)
        for tag in page_tags:
            page_data['tags'].append(tag)

        page_languages: list[str] = Parse.get_language(work_list)
        for lang in page_languages:
            page_data['language'].append(lang)

        page_words: list[int] = Parse.get_words(work_list)
        for words in page_words:
            page_data['words'].append(words)

        page_chapters: list[int] = Parse.get_chapters(work_list)
        for chaps in page_chapters:
            page_data['chapters'].append(chaps)

        page_collections: list[int] = Parse.get_collections(work_list)
        for collect in page_collections:
            page_data['collections'].append(collect)

        page_comments: list[int] = Parse.get_comments(work_list)
        for comments in page_comments:
            page_data['comments'].append(comments)

        page_kudos: list[int] = Parse.get_kudos(work_list)
        for kud in page_kudos:
            page_data['kudos'].append(kud)

        page_bookmarks: list[int] = Parse.get_bookmarks(work_list)
        for marks in page_bookmarks:
            page_data['bookmarks'].append(marks)

        page_hits: list[int] = Parse.get_hits(work_list)
        for hit in page_hits:
            page_data['hits'].append(hit)

        page_series: list[str] = Parse.get_series(work_list)
        for part in page_series:
            page_data['series'].append(part)

        return page_data
