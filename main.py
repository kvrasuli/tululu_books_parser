import requests
from pathlib import Path
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin
import json
from parse_tululu_category import parse_category
import argparse
import sys
import logging


def main():
    logging.basicConfig(filename='app.log', filemode='w')
    start_page, end_page, dest_folder, \
        skip_img, skip_txt, json_path = parse_arguments()
    books = []
    book_ids = parse_category(start_page, end_page)
    for number, book_id in enumerate(book_ids):
        try:
            txt_url = f'http://tululu.org/txt.php?id={book_id}'
            title, author, pic_name, \
                comments, genres = parse_book_page(book_id)
            pic_url = urljoin('http://tululu.org/', pic_name)
            filename = f'{book_id}. {title}'
            if not skip_txt:
                book_path = download_txt(txt_url, filename, Path(dest_folder))
            else:
                book_path = None
            if not skip_img:
                img_path = download_image(pic_url, filename, Path(dest_folder))
            else:
                img_path = None
        except Exception as e:
            logging.warning(str(e))
            print(str(e), file=sys.stderr)
        finally:
            books.append({
                'title': title,
                'author': author,
                'img_src': img_path,
                'comments': book_path,
                'genres': comments,
                'book_path': genres,
            })
    json_path = Path(json_path).joinpath('books.json')
    with open(json_path, 'w', encoding='utf8') as json_file:
        json.dump(books, json_file, ensure_ascii=False)


def parse_arguments():
    parser = argparse.ArgumentParser(description='Tululu books parser')
    parser.add_argument(
        '--start_page', help='Start page to parse', default=1, type=int
    )

    parser.add_argument(
        '--end_page', help='End page to parse', default=5, type=int
    )
    parser.add_argument(
        '--dest_folder',
        help='End page to parse',
        default='books/'
    )
    parser.add_argument(
        '--skip_img',
        help='Skip downloading images',
        action='store_true'
    )
    parser.add_argument(
        '--skip_txt',
        help='Skip dowloading books',
        action='store_true'
    )
    parser.add_argument('--json_path', help='JSON path', default='')

    arguments = parser.parse_args()
    start_page = arguments.start_page
    end_page = arguments.end_page
    dest_folder = arguments.dest_folder
    skip_img = arguments.skip_img
    skip_txt = arguments.skip_txt
    json_path = arguments.json_path
    return start_page, end_page, dest_folder, skip_img, skip_txt, json_path


def parse_book_page(book_id):
    response = requests.get(f'http://tululu.org/b{book_id}/')
    book_image_selector = '.bookimage a img'
    book_title_selector = 'h1'
    book_comments_selector = '.texts .black'
    book_genre_selector = '.d_book > a'
    comments = []
    genres = []
    check_response()
    soup = BeautifulSoup(response.text, 'lxml')
    pic = soup.select_one(book_image_selector)['src']
    title = soup.select_one(book_title_selector).text.split('::')[0].strip()
    author = soup.select_one(book_title_selector).text.split('::')[1].strip()

    for comment in soup.select(book_comments_selector):
        comments.append(comment.text)

    for genre in soup.select(book_genre_selector):
        genres.append(genre.text)
    return title, author, pic, comments, genres


def download_txt(url, filename, folder):
    Path(folder).mkdir(parents=True, exist_ok=True)
    response = requests.get(url)
    sanitized_filename = sanitize_filename(filename)
    check_response()
    path_to_save = Path(folder).joinpath(f'{sanitized_filename}.txt')
    with open(path_to_save, 'wb') as book:
        book.write(response.content)
    return str(path_to_save)


def download_image(url, filename, folder):
    Path(folder).mkdir(parents=True, exist_ok=True)
    response = requests.get(url)
    sanitized_filename = sanitize_filename(filename)
    check_response()
    img_extension = Path(url).suffix
    full_filename = f'{sanitized_filename}{img_extension}'
    path_to_save = Path(folder).joinpath(full_filename)
    with open(path_to_save, 'wb') as image:
        image.write(response.content)
    return str(path_to_save)


def check_response(response):
    response.raise_for_status()
    if response.url == 'http://tululu.org/':
        raise Exception()
    # (f"Book {sanitized_filename} hasn't been downloaded!")
        # raise Exception(f"Cover {sanitized_filename} \
        #             hasn't been downloaded!")
        # raise Exception(f"Book page {book_id} hasn't been parsed!")


if __name__ == '__main__':
    main()
