import requests
from pathlib import Path
from bs4 import BeautifulSoup
import lxml
from pathvalidate import sanitize_filename

def main():
    for book_id in range(1, 11):
        url = f'http://tululu.org/txt.php?id={book_id}'
        title = get_title(book_id)
        if title is not None:
            download_txt(url, f'{book_id}. {title}')

def get_title(book_id):
    title = None
    response = requests.get(f'http://tululu.org/b{book_id}/')
    response.raise_for_status()
    if response.url != 'http://tululu.org/':
        soup = BeautifulSoup(response.text, 'lxml')
        title = soup.find('h1').text.split('::')[0].strip()
    return title

def download_txt(url, filename, folder='books/'):
    Path(folder).mkdir(parents=True, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    if response.url != 'http://tululu.org/':
        sanitized_filename = sanitize_filename(filename)
        path_to_save = Path(folder).joinpath(f'{sanitized_filename}.txt')
        with open(path_to_save, 'wb') as book:
            book.write(response.content)
        return path_to_save





if __name__ == '__main__':
    main()