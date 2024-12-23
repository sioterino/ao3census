from pandas import DataFrame
from utils import Utils


class Ordered:
    @staticmethod
    def most_of(df: DataFrame, header) -> dict[str, int]:
        cells = df[header]
        output: dict[str, int] = {}

        match header:
            case 'warnings' | 'orientations':
                for cell_str in cells:
                    cells = eval(cell_str)
                    for string in cells:
                        elements = string.split(',')
                        for item in elements:
                            append_2dict(item.strip(), output)


            case __:
                for cell_str in cells:
                    if '[' in cell_str and ']' in cell_str:
                        cell = eval(cell_str)
                        for item in cell:
                            if 'orphan_account' not in item:
                                append_2dict(item, output)
                    else:
                        append_2dict(cell_str, output)

        return Utils.order_dict_by_value(output)


def append_2dict(item, dictionary):
    if item in dictionary:
        dictionary[item] += 1
    else:
        dictionary[item] = 1
