import requests
import xmltodict
from logging import getLogger, StreamHandler, Formatter, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)

class OpenLibraryAPI:
    def __init__(self, timeout=1, verbose=False):
        self.base_url = 'https://openlibrary.org'
        self.timeout = timeout
        self.verbose = verbose

    def isbn_search(self, isbn):
        if self.verbose:logger.info(f'Searching for book with ISBN: {isbn}')
        try:
            response = requests.get(f'{self.base_url}/isbn/{isbn}.json', timeout=self.timeout)
        except requests.exceptions.Timeout:
            if self.verbose:logger.error('Request timed out')
            return None
        except requests.exceptions.ConnectionError:
            if self.verbose:logger.error('Connection error')
            return None
        except:
            if self.verbose:logger.error('Unknown error')
            return None
        if response.status_code == 200:
            if self.verbose:logger.info('Request succeeded')
            return response.json()
        else:
            if self.verbose:logger.error('Request failed')
            return None
        
    def author_search(self, author_key):
        if self.verbose:logger.info(f'Searching for books by author: {author_key}')
        try:
            response = requests.get(f'{self.base_url}{author_key}.json', timeout=self.timeout)
        except requests.exceptions.Timeout:
            if self.verbose:logger.error('Request timed out')
            return None
        except requests.exceptions.ConnectionError:
            if self.verbose:logger.error('Connection error')
            return None
        except:
            if self.verbose:logger.error('Unknown error')
            return None
        if response.status_code == 200:
            if self.verbose:logger.info('Request succeeded')
            return response.json()
        else:
            if self.verbose:logger.error('Request failed')
            return None

        
class GoogleBooksAPI:
    def __init__(self, timeout=1, verbose=False):
        self.base_url = 'https://www.googleapis.com/books/v1'
        self.timeout = timeout
        self.verbose = verbose

    def isbn_search(self, isbn):
        if self.verbose:logger.info(f'Searching for book with ISBN: {isbn}')
        try:
            response = requests.get(f'{self.base_url}/volumes?q=isbn:{isbn}', timeout=self.timeout)
        except requests.exceptions.Timeout:
            if self.verbose:logger.error('Request timed out')
            return None
        except requests.exceptions.ConnectionError:
            if self.verbose:logger.error('Connection error')
            return None
        except:
            if self.verbose:logger.error('Unknown error')
            return None
        if response.status_code == 200:
            if self.verbose:logger.info('Request succeeded')
            return response.json()
        else:
            if self.verbose:logger.error('Request failed')
            return None

class NDLAPI:
    def __init__(self, timeout=1, verbose=False):
        self.base_url = 'https://iss.ndl.go.jp/api/sru'
        self.timeout = timeout
        self.verbose = verbose

    def isbn_search(self, isbn):
        if self.verbose:logger.info(f'Searching for book with ISBN: {isbn}')
        params = {'operation': 'searchRetrieve', 'query': f'isbn="{isbn}"', 'recordPacking': 'xml'}
        try:
            response = requests.get(f'{self.base_url}', params=params, timeout=self.timeout)
        except requests.exceptions.Timeout:
            if self.verbose:logger.error('Request timed out')
            return None
        except requests.exceptions.ConnectionError:
            if self.verbose:logger.error('Connection error')
            return None
        except:
            if self.verbose:logger.error('Unknown error')
            return None
        if response.status_code == 200:
            if self.verbose:logger.info('Request succeeded')
            return xmltodict.parse(response.text)
        else:
            if self.verbose:logger.error('Request failed')
            return None

class OpenBDAPI:
    def __init__(self, timeout=1, verbose=False):
        self.base_url = 'https://api.openbd.jp/v1'
        self.timeout = timeout
        self.verbose = verbose

    def isbn_search(self, isbn):
        if self.verbose:logger.info(f'Searching for book with ISBN: {isbn}')
        try:
            response = requests.get(f'{self.base_url}/get', params={'isbn': isbn}, timeout=self.timeout)
        except requests.exceptions.Timeout:
            if self.verbose:logger.error('Request timed out')
            return None
        except requests.exceptions.ConnectionError:
            if self.verbose:logger.error('Connection error')
            return None
        except:
            if self.verbose:logger.error('Unknown error')
            return None
        if response.status_code == 200:
            if self.verbose:logger.info('Request succeeded')
            return response.json()
        else:
            if self.verbose:logger.error('Request failed')
            return None

def isbn10_to_isbn13(isbn10:str) -> str:
    """ISBN10をISBN13に変換する
    
    Args:
        isbn10 (str): ISBN10
        
    Returns:
        str: ISBN13
    """
    isbn10 = only_number(str(isbn10))
    if len(isbn10) != 10:
        raise ValueError(f"ISBN10の長さが不正です. isnb_10={isbn10}")
    
    # "978"を先頭に追加し、チェックディジットを除いた部分を取得
    isbn13_body = "978" + isbn10[:-1]
    
    # ISBN13のチェックディジットを計算
    check_digit = 0
    for i, digit in enumerate(isbn13_body):
        check_digit += int(digit) * (1 if i % 2 == 0 else 3)
    check_digit = (10 - (check_digit % 10)) % 10
    
    return isbn13_body + str(check_digit)

def isbn13_to_isbn10(isbn13:str) -> str:
    """ISBN13をISBN10に変換する

    Args:
        isbn13 (str): ISBN13

    Returns:
        str: ISBN10
    """
    isbn13 = only_number(str(isbn13))
    if len(isbn13) != 13 or not isbn13.startswith("978"):
        raise ValueError(f"ISBN13のフォーマットが不正です. isbn_13={isbn13}")
    
    # ISBN13の4〜12桁を使ってチェックディジットを除いた部分を取得
    isbn10_body = isbn13[3:-1]
    
    # ISBN10のチェックディジットを計算
    check_digit = 0
    for i, digit in enumerate(isbn10_body):
        check_digit += int(digit) * (10 - i)
    check_digit = (11 - (check_digit % 11)) % 11
    
    # チェックディジットが10の場合は "X"
    if check_digit == 10:
        check_digit = "X"
    
    return isbn10_body + str(check_digit)

def only_number(number:str) -> str:
    """文字列からISBNで利用されている文字のみを取り出す
    
    Args:
        number (str): 数字を含む文字列
        
    Returns:
        str: 数字のみを取り出した文字列
    """
    if number[-1] == "X":
        number = number[:-1]
        last = "X"
    else:
        last = ""
    return ''.join(filter(str.isdecimal, number)) + last

def calc_both_isbn(isbn:str|int) -> tuple:
    """ISBN10とISBN13の両方を計算する

    Args:
        isbn (str|int): ISBN10またはISBN13

    Returns:
        tuple: ISBN10, ISBN13
    """
    if isinstance(isbn, int):
        isbn = str(isbn)
    elif not isinstance(isbn, str):
        raise ValueError("ISBNは文字列か数値で指定してください")
    isbn_number = only_number(isbn)
    if len(isbn_number) == 10:
        isbn10 = isbn_number
        isbn13 = isbn10_to_isbn13(isbn10)
    elif len(isbn_number) == 13:
        isbn13 = isbn_number
        isbn10 = isbn13_to_isbn10(isbn13)
    else:
        raise ValueError("ISBNの桁数が不正です")
    return isbn10, isbn13
