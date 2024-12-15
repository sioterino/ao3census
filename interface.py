from InquirerPy.validator import PathValidator
from InquirerPy.base.control import Choice
from InquirerPy import inquirer as iq

import os

from utils import Utils


class Interface:
    @staticmethod
    def scanner(user_data: dict):

        user_data['scrape']: bool = will_scrape()

        if not user_data['scrape']:
            user_data['file_path']: str = get_file_path(user_data['scrape'])

        if user_data['scrape']:
            user_data['login']: bool = will_log_in()

            if user_data['login']:
                user_data['username']: str = get_username()
                user_data['password']: str = get_password()

            user_data['fandom'] = get_fandom()

            user_data['is_category']: bool = is_categorized()

            if user_data['is_category']:
                user_data['category'] = get_category()

        return user_data


def will_log_in() -> bool:
    boolean: bool = iq.select(
        message='Do you want to log in your AO3 account to access more stories?',
        choices=[
            Choice(value=True, name='Yes', enabled=True),
            Choice(value=False, name='No'),
            Choice(value=None, name='Exit'),
        ],
        default=True
    ).execute()

    if boolean is None:
        exit(0)

    return boolean


def get_username() -> str:
    return iq.text(message='Username: ').execute()


def get_password() -> str:
    return iq.secret(message='Password: ').execute()


def get_fandom() -> str:
    fandom: str = iq.text(message='Intended fandom name: ').execute()
    fandom = Utils.fandom_name(fandom)
    return fandom


def is_categorized() -> bool:
    boolean: bool = iq.select(
        message='Does your fandom have a category?',
        choices=[
            Choice(value=True, name='Yes', enabled=True),
            Choice(value=False, name='No'),
            Choice(value=None, name='Exit'),
        ],
        default=True
    ).execute()

    if boolean is None:
        exit(0)

    return boolean


def get_category() -> str:
    return iq.select(
        message="What is your fandom's category name",
        choices=[
            Choice(value='Band', name='Band', enabled=True),
        ],
        default=True
    ).execute()


def will_scrape() -> bool:
    boolean: bool = iq.select(
        message='Do you want to web scrape?',
        choices=[
            Choice(value=True, name='Yes', enabled=True),
            Choice(value=False, name='No'),
            Choice(value=None, name='Exit'),
        ],
        default=True
    ).execute()

    if boolean is None:
        exit(0)

    return boolean


def get_file_path(scrape: bool) -> str:
    file_path: str = ''
    while True:
        if not scrape:
            file_path = input_path()
        if Utils.validate_file_extension(file_path, '.csv'):
            break
    return file_path


def input_path() -> str:
    bar: str = '/' if os.name == 'posix' else '\\'
    home_path = f'{os.getcwd()}{bar}results{bar}'
    return iq.filepath(
        message="Enter file or directory to upload:",
        default=home_path,
        validate=PathValidator(is_file=True, message="Input is not a file"),
        multicolumn_complete=True
    ).execute()
