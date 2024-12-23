from pandas import DataFrame


class Basics:
    @staticmethod
    def number_of_works(df: DataFrame) -> int:
        return len(df.index)

    @staticmethod
    def get_totals(df: DataFrame, header: str) -> int:
        return df[header].sum()

    @staticmethod
    def get_lowercases(df: DataFrame) -> list[str]:
        titles: list[str] = df['title']
        lowercased: list[str] = []

        for title in titles:
            if title.islower():
                lowercased.append(title)

        return lowercased

    @staticmethod
    def get_orphans(df: DataFrame) -> dict[str, int]:
        authors: list = df['authors']
        anonymous: int = 0
        orphaned: int = 0

        for work_authors in authors:
            if not eval(work_authors):
                anonymous += 1
                continue
            if "orphan_account" in work_authors:
                orphaned += 1

        return {'orphaned': orphaned, 'anonymous': anonymous}
