from bs4 import BeautifulSoup


class Parse:
    @staticmethod
    def get_titles(work_list: list) -> list[str]:
        titles: list[str] = []
        for work in work_list:
            title: str = work.find('div', class_='header module').find('h4', class_='heading').find('a').text
            titles.append(title)
        return titles

    @staticmethod
    def get_authors(work_list: list) -> list[str]:
        authors: list = []
        for work in work_list:
            author_tags: list = work.find('div', class_='header module').find('h4', class_='heading').find_all(rel="author")
            authors.append([author.text for author in author_tags])
        return authors

    @staticmethod
    def get_fandoms(work_list: list, fandom_name: str) -> list[str]:
        fandoms: list = []
        for work in work_list:
            fandom_tags: list = work.find('div', class_='header module').find('h5', class_='fandoms heading').find_all('a')
            fandoms.append([fandom.text for fandom in fandom_tags])
        return remove_original_fandom(fandoms, fandom_name)

    @staticmethod
    def get_ratings(work_list: list) -> list[str]:
        ratings: list[str] = []
        for work in work_list:
            ratings.extend(get_required_tags(work)[0])
        return ratings

    @staticmethod
    def get_warnings(work_list: list) -> list[str]:
        warnings: list[str] = []
        for work in work_list:
            warnings.append(get_required_tags(work)[1])
        return warnings

    @staticmethod
    def get_orientations(work_list: list) -> list[str]:
        orientations: list[str] = []
        for work in work_list:
            orientations.append(get_required_tags(work)[2])
        return orientations

    @staticmethod
    def get_status(work_list: list) -> list[str]:
        status: list[str] = []
        for work in work_list:
            status.extend(get_required_tags(work)[3])
        return status

    @staticmethod
    def get_updates(work_list: list) -> list[str]:
        updates: list[str] = []
        for work in work_list:
            update: str = work.find('p', class_='datetime').text
            updates.append(update)
        return updates

    @staticmethod
    def get_ships(work_list: list) -> list[str]:
        ships: list = []
        for work in work_list:
            ship_tags: list = work.find('ul', class_='tags commas').find_all('li', class_='relationships')
            ships.append([ship.text for ship in ship_tags])
        return ships

    @staticmethod
    def get_chars(work_list: list) -> list[str]:
        chars: list = []
        for work in work_list:
            char_tags: list = work.find('ul', class_='tags commas').find_all('li', class_='characters')
            chars.append([ship.text for ship in char_tags])
        return chars

    @staticmethod
    def get_freeform_tags(work_list: list) -> list[str]:
        tags: list = []
        for work in work_list:
            tag_tags: list = work.find('ul', class_='tags commas').find_all('li', class_='freeforms')
            tags.append([ship.text for ship in tag_tags])
        return tags

    @staticmethod
    def get_language(work_list: list) -> list[str]:
        languages: list = []
        for work in work_list:
            language: str = work.find('dl', class_='stats').find('dd', class_='language').text
            languages.append(language)
        return languages

    @staticmethod
    def get_words(work_list: list) -> list[int]:
        words: list[int] = []
        for work in work_list:
            word: str = work.find('dl', class_='stats').find('dd', class_='words').text \
                if work.find('dl', class_='stats').find('dd', class_='words') else '0'
            words.append(str2int(word))
        return words

    @staticmethod
    def get_chapters(work_list: list) -> list[int]:
        chapters: list[int] = []
        for work in work_list:
            chaps: str = work.find('dl', class_='stats').find('dd', class_='chapters').text \
                if work.find('dl', class_='stats').find('dd', class_='chapters') else '0'
            chapters.append(str2int(chaps.split('/')[0]))
        return chapters

    @staticmethod
    def get_collections(work_list: list) -> list[int]:
        collections: list[int] = []
        for work in work_list:
            collect: str = work.find('dl', class_='stats').find('dd', class_='collections').text \
                if work.find('dl', class_='stats').find('dd', class_='collections') else '0'
            collections.append(str2int(collect))
        return collections

    @staticmethod
    def get_comments(work_list: list) -> list[int]:
        comments: list[int] = []
        for work in work_list:
            comment: str = work.find('dl', class_='stats').find('dd', class_='comments').text \
                if work.find('dl', class_='stats').find('dd', class_='comments') else '0'
            comments.append(str2int(comment))
        return comments

    @staticmethod
    def get_kudos(work_list: list) -> list[int]:
        kudos: list[int] = []
        for work in work_list:
            kud: str = work.find('dl', class_='stats').find('dd', class_='kudos').text \
                if work.find('dl', class_='stats').find('dd', class_='kudos') else '0'
            kudos.append(str2int(kud))
        return kudos

    @staticmethod
    def get_bookmarks(work_list: list) -> list[int]:
        bookmarks: list[int] = []
        for work in work_list:
            mark: str = work.find('dl', class_='stats').find('dd', class_='bookmarks').text \
                if work.find('dl', class_='stats').find('dd', class_='bookmarks') else '0'
            bookmarks.append(str2int(mark))
        return bookmarks

    @staticmethod
    def get_hits(work_list: list) -> list[int]:
        hits: list[int] = []
        for work in work_list:
            hit: str = work.find('dl', class_='stats').find('dd', class_='hits').text \
                if work.find('dl', class_='stats').find('dd', class_='hits') else '0'
            hits.append(str2int(hit))
        return hits

    @staticmethod
    def get_series(work_list: list) -> list[str]:
        series: list[str] = []
        for work in work_list:
            part: str = work.find('ul', class_='series').find('li').text \
                if work.find('ul', class_='series') else ''
            series.append(part.strip())
        return series


def remove_original_fandom(fandoms: list, fandom_name: str) -> list:
    for tags in fandoms:
        if fandom_name in tags:
            tags.remove(fandom_name)
    return fandoms


def get_required_tags(work: BeautifulSoup):
    a_tags: list = work.findAll('a', class_='help symbol question modal')
    text: list = []
    for a in a_tags:
        span: str = a.find('span', class_='text').text
        text.append([span])
    return text


def str2int(num: str) -> int:
    if ',' in num:
        return int(num.replace(",", ""))
    elif '.' in num:
        return int(num.replace(".", ""))
    else:
        return int(num)
