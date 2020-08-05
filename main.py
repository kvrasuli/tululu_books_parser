import requests
from itertools import count
from pathlib import Path


def main():
    Path('books').mkdir(parents=True, exist_ok=True)
    for id in count(1):
        url = f'http://tululu.org/txt.php?id={id}'
        response = requests.get(url)
        if response.url != 'http://tululu.org/':
            with open(f'books/book_{id}.txt', 'wb') as book:
                book.write(response.content)

        if id == 10: 
            break


if __name__ == '__main__':
    main()