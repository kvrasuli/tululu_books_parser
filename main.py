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
from check_response import check_response, TululuResponseError


def main():
    logging.basicConfig(filename='app.log', filemode='w')
    start_page, end_page, dest_folder, \
        skip_img, skip_txt, json_path = parse_arguments()
    books = []
    try:
        book_ids = parse_category(start_page, end_page)
    except TululuResponseError as e:
        logging.error(str(e))
        print(str(e), file=sys.stderr)
        sys.exit()

    for book_id in book_ids:
        try:
            title, author, pic_url, \
                comments, genres = parse_book_page(book_id)
        except TululuResponseError as e:
            logging.error(str(e))
            print(str(e), file=sys.stderr)

        filename = f'{book_id}. {title}'
        txt_url = f'http://tululu.org/txt.php?id={book_id}'
        if not skip_txt:
            try:
                book_path = download_txt(
                    txt_url,
                    filename,
                    Path(dest_folder)
                )
            except TululuResponseError as e:
                book_path = None
                logging.error(str(e))
                print(str(e), file=sys.stderr)
        else:
            book_path = None

        pic_url = urljoin(f'http://tululu.org/{book_id}/shots', pic_url)
        if not skip_img:
            try:
                img_path = download_image(
                    pic_url,
                    filename,
                    Path(dest_folder)
                )
            except TululuResponseError as e:
                img_path = None
                logging.error(str(e))
                print(str(e), file=sys.stderr)
        else:
            img_path = None

        books.append({
            'title': title,
            'author': author,
            'img_src': img_path,
            'comments': comments,
            'genres': genres,
            'book_path': book_path,
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
    error_message = f"Book page {book_id} hasn't been parsed!"
    check_response(response, error_message)
    soup = BeautifulSoup(response.text, 'lxml')
    pic = soup.select_one(book_image_selector)['src']
    title = soup.select_one(book_title_selector).text.split('::')[0].strip()
    author = soup.select_one(book_title_selector).text.split('::')[1].strip()
    comments = [comment.text for comment in soup.select(book_comments_selector)]
    genres = [genre.text for genre in soup.select(book_genre_selector)]
    return title, author, pic, comments, genres


def download_txt(url, filename, folder):
    Path(folder).mkdir(parents=True, exist_ok=True)
    response = requests.get(url)
    sanitized_filename = sanitize_filename(filename)
    error_message = f"Book {sanitized_filename} hasn't been downloaded!"
    check_response(response, error_message)
    path_to_save = Path(folder).joinpath(f'{sanitized_filename}.txt')
    with open(path_to_save, 'wb') as book:
        book.write(response.content)
    return str(path_to_save)


def download_image(url, filename, folder):
    if not Path(folder).joinpath(filename + '.txt').is_file():
        return
    Path(folder).mkdir(parents=True, exist_ok=True)
    response = requests.get(url)
    sanitized_filename = sanitize_filename(filename)
    error_message = f"Cover {sanitized_filename} hasn't been downloaded!"
    check_response(response, error_message)
    img_extension = Path(url).suffix
    full_filename = f'{sanitized_filename}{img_extension}'
    path_to_save = Path(folder).joinpath(full_filename)
    with open(path_to_save, 'wb') as image:
        image.write(response.content)
    return str(path_to_save)


if __name__ == '__main__':
    main()
