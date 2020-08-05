import requests
from bs4 import BeautifulSoup


def parse_category():
    ids = []
    for page in range(1, 2):
        url = f'http://tululu.org/l55/{page}'
        response = requests.get(url)
        response.raise_for_status()
        book_src_selector = '.bookimage > a'
        if response.url != 'http://tululu.org/':
            soup = BeautifulSoup(response.text, 'lxml')
            for src in soup.select(book_src_selector):
                ids.append(src['href'][2:-1])
    # print(ids)
    return ids


if __name__ == '__main__':
    parse_category()
