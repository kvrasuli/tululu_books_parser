import requests
from itertools import count
from pathlib import Path
from bs4 import BeautifulSoup
import lxml


def main():
    Path('books').mkdir(parents=True, exist_ok=True)
    for id in count(1):
        url = f'http://tululu.org/txt.php?id={id}'
        response = requests.get(url)
        response.raise_for_status()
        if response.url != 'http://tululu.org/':
            author, title = get_author_and_title(id)
            print(author, title)
            with open(f'books/{title}_{author}.txt', 'wb') as book:
                book.write(response.content)

        if id == 10: 
            break


def get_author_and_title(id):
    response = requests.get(f'http://tululu.org/b{id}/')
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    author = soup.find('h1').text.split('::')[0].strip()
    title = soup.find('h1').text.split('::')[1].strip()
    return author, title

if __name__ == '__main__':
    main()