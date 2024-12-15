from requests import Session, Response
from bs4 import BeautifulSoup

from time import sleep

from .get_page import GetPage


class Login:
    @staticmethod
    def login(session: Session, uname: str, upswd: str):
        token = get_token(session)
        payload = {
            "utf8": "✓",
            "authenticity_token": token,
            "user[login]": uname,
            "user[password]": upswd,
            "commit": "Log in"
        }
        post = session.post("https://archiveofourown.org/users/login", data=payload)
        GetPage.checks_sc(post.status_code)

    @staticmethod
    def try_logging_in(session: Session, username: str, password: str, login_limit: int):
        is_logged_in: bool = False
        attempts: int = 0

        while not is_logged_in:
            if attempts <= login_limit:
                Login.login(session, username, password)
                attempts += 1
                print(attempts)
            else:
                print('didnt logged in')
                break

            response_test: Response = session.get(f"https://archiveofourown.org/users/{username}/readings")
            soup_test: BeautifulSoup = BeautifulSoup(response_test.content, "html.parser")
            if not soup_test.find("a", {"href": f"/users/{username}"}):
                is_logged_in = False
                continue

            print('logged in')
            is_logged_in = True


def get_token(session: Session) -> list[str]:
    sleep(6)
    response = session.get("https://archiveofourown.org")
    soup = BeautifulSoup(response.content, "html.parser")
    return soup.find("meta", {"name": "csrf-token"})["content"]
