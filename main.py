import requests
from pathlib import Path
from bs4 import BeautifulSoup
import lxml
from pathvalidate import sanitize_filename
from urllib.parse import urljoin
import json
from parse_tululu_category import parse_category
import pprint

def main():
    books = []
    book_ids = parse_category()
    for number, book_id in enumerate(book_ids):
        books.append({
            'title': '',
            'author': '',
            'img_src': '',
            'comments': '',
            'genres': '',
            'book_path': ''
        })
        try:
            txt_url = f'http://tululu.org/txt.php?id={book_id}'
            title, author, pic_name, comments, genres = parse_book_page(book_id)
            pic_url = urljoin('http://tululu.org/', pic_name)
            book_path = download_txt(txt_url, f'{book_id}. {title}')
            img_path = download_image(pic_url, f'{book_id}. {title}')
            books[number]['title'] = title
            books[number]['author'] = author
            books[number]['img_src'] = img_path
            books[number]['book_path'] = book_path
            books[number]['comments'] = comments
            books[number]['genres'] = genres
        except:
            pass
            
    with open('books.json', 'w', encoding='utf8') as json_file:
        json.dump(books, json_file, ensure_ascii=False)

def parse_book_page(book_id):
    response = requests.get(f'http://tululu.org/b{book_id}/')
    response.raise_for_status()
    book_image_selector = '.bookimage a img'
    book_title_selector = 'h1'
    book_comments_selector = '.texts .black'
    book_genre_selector = '.d_book > a'
    comments = []
    genres = []
    if response.url != 'http://tululu.org/':
        soup = BeautifulSoup(response.text, 'lxml')
        pic = soup.select_one(book_image_selector)['src']
        title = soup.select_one(book_title_selector).text.split('::')[0].strip()
        author = soup.select_one(book_title_selector).text.split('::')[1].strip()

        for comment in soup.select(book_comments_selector):
            comments.append(comment.text)

        for genre in soup.select(book_genre_selector):
            genres.append(genre.text)
        return title, author, pic, comments, genres

def download_txt(url, filename, folder='books/'):
    Path(folder).mkdir(parents=True, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    if response.url != 'http://tululu.org/':
        sanitized_filename = sanitize_filename(filename)
        path_to_save = Path(folder).joinpath(f'{sanitized_filename}.txt')
        with open(path_to_save, 'wb') as book:
            book.write(response.content)
        return str(path_to_save)


def download_image(url, filename, folder='images/'):
    Path(folder).mkdir(parents=True, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    if response.url != 'http://tululu.org/':
        sanitized_filename = sanitize_filename(filename)
        img_extension = Path(url).suffix
        path_to_save = Path(folder).joinpath(f'{sanitized_filename}{img_extension}')
        with open(path_to_save, 'wb') as image:
            image.write(response.content)
        return str(path_to_save)


if __name__ == '__main__':
    main()