from zipfile import ZipFile
import wget
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import ftplib
from datetime import date, timedelta
import pandas as pd

# textbook url 'http://www.pythonscraping.com/pages/page1.html'


def scraping_links_from_urls(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        print(e)
    except URLError as e:
        url = input('Please check the url and re-enter')
        html = urlopen(url)

    bsObj = BeautifulSoup(html.read(), features="html.parser")
    links = []
    for link in bsObj.findAll('a'):
        link = link.get('href')
        if link not in links:
            links.append(link)

    return links


def get_and_unzip(url_of_file, destination_path, zipped_file_path):
    wget.download(url_of_file, destination_path)
    ZipFile(zipped_file_path, 'r').extractall(destination_path)
    return
