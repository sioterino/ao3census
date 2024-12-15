from requests import Response, Session
from bs4 import BeautifulSoup


class GetPage:
    @staticmethod
    def get_html_of_page(session: Session, url: str) -> BeautifulSoup:
        response: Response = access_page(session=session, url=url)
        return BeautifulSoup(response.content, 'html.parser')

    @staticmethod
    def checks_sc(status_code):
        match status_code:
            case 200:
                pass
            case 404:
                print("404 Page not Found")
                exit(1)
            case __:
                print(f"unexpected sc: {status_code}")
                exit(1)


def access_page(session: Session, url: str) -> Response:
    response: Response = session.get(url)
    GetPage.checks_sc(response.status_code)
    return response
