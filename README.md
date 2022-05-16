# Parser of books from tululu.org

Console app for parsing and downloading books and their covers from the sci-fi section of [tululu.org](https://dvmn.org/).
Additional information is stored in a JSON file.

### How to use
- Install dependencies:
```
pip3 install -r requirements.txt
```
- Run the script with arguments (see below):
```
python3 main.py --start_page [start_page] --end_page [end_page]
```

### Arguments
The script accepts 2 optional arguments - the first page number and the last page number of tululu.org,
for example:

```
python3 main.py --start_page 700 --end_page 705
```
By default only first five pages are downloaded.
Other optional arguments:
```
--dest_folder [path_to_folder] - download path
--skip_img - don't download images
--skip_txt - don't download books
--json_path [path_to_json] - path to the json file
```
