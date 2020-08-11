import requests
from bs4 import BeautifulSoup
import argparse
from check_response import check_response


def parse_category(start_page, end_page):
    for page in range(start_page, end_page + 1):
        url = f'http://tululu.org/l55/{page}'
        response = requests.get(url)
        response.raise_for_status()
        book_src_selector = '.bookimage > a'
        error_message = "Category hasn't been parsed!"
        check_response(response, error_message)
        soup = BeautifulSoup(response.text, 'lxml')
        ids = [src['href'][2:-1] for src in soup.select(book_src_selector)]
    return ids


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tululu books parser')
    parser.add_argument('--start_page', help='Start page to parse', default=1, type=int)
    parser.add_argument('--end_page', help='End page to parse', default=5, type=int)
    arguments = parser.parse_args()
    start_page = arguments.start_page
    end_page = arguments.end_page
    parse_category(start_page, end_page)
