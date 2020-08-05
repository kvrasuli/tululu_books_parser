import requests
from pathlib import Path
from bs4 import BeautifulSoup
import lxml
from pathvalidate import sanitize_filename
from urllib.parse import urljoin

def main():
    for book_id in range(1, 11):
        try:
            txt_url = f'http://tululu.org/txt.php?id={book_id}'
            title, pic_name = get_title(book_id)
            pic_url = urljoin('http://tululu.org/', pic_name)
  
            download_txt(txt_url, f'{book_id}. {title}')
            download_image(pic_url, f'{book_id}. {title}')
        except:
            pass

def get_title(book_id):
    response = requests.get(f'http://tululu.org/b{book_id}/')
    response.raise_for_status()
    book_image_selector = '.bookimage a img'
    book_title_selector = 'h1'
    if response.url != 'http://tululu.org/':
        soup = BeautifulSoup(response.text, 'lxml')
        # title = soup.find('h1').text

        pic = soup.select_one(book_image_selector)['src']
        title = soup.select_one(book_title_selector).text.split('::')[0].strip()
        
        return title, pic

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


def download_image(url, filename, folder='images/'):
    Path(folder).mkdir(parents=True, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    if response.url != 'http://tululu.org/':
        sanitized_filename = sanitize_filename(filename)
        img_extension = Path(url).suffix
        path_to_save = Path(folder).joinpath(f'{sanitized_filename}.{img_extension}')
        with open(path_to_save, 'wb') as image:
            image.write(response.content)
        return path_to_save





if __name__ == '__main__':
    main()