from datetime import datetime

class Parse:
    def get_titles(work_list: list) -> list:
        titles: list = []
        for work in work_list:
            title: list = work.find('div', class_='header module').find('h4', class_='heading').find('a').text
            titles.append(title)
        return titles

    def get_authors(work_list: list) -> list:
        authors: list = []
        for work in work_list:
            author_tags: list = work.find('div', class_='header module').find('h4', class_='heading').find_all(rel="author")
            author_names = [author.text for author in author_tags]
            authors.append(author_names)
        return authors

if __name__ == '__main__':
    print()