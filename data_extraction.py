from zipfile import ZipFile
import wget
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import ftplib
from datetime import date, timedelta
import pandas as pd


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


def get_cme_settle(ftp_url='ftp.cmegroup.com', ftp_cwd='pub/settle', download_path='ftp_cme_downloads/'):
    ftp = ftplib.FTP(ftp_url)
    ftp.login()
    ftp.cwd(ftp_cwd)
    now = date.today()
    yesterday = now - timedelta(1)
    already_downloaded = pd.read_csv(f'all_files_cme_{yesterday}', index_col=0, names=['files'])
    already_downloaded = already_downloaded['files'].to_list()
    todays_files = ftp.nlst()
    files_to_download = [i for i in todays_files if i not in already_downloaded]
    for i in files_to_download:
        wget.download(f'{ftp_url}/{ftp_cwd}/{i}', download_path)
        if i.endswith('.zip'):
            ZipFile(f'{i}', 'r').extractall(download_path)
        already_downloaded = already_downloaded.append(i)

    # save new already_downloaded list to file
    pd.DataFrame(already_downloaded).to_csv(f'all_files_cme_{now.day}')
    # delete old already_downloaded list

    # close ftp
    ftp.close()


def get_and_unzip(url_of_file, destination_path, zipped_file_path):
    wget.download(url_of_file, destination_path)
    ZipFile(zipped_file_path, 'r').extractall(destination_path)
    return




# textbook url 'http://www.pythonscraping.com/pages/page1.html'
# ftp://ftp.cmegroup.com/pub/settle/Expiring_Options_UnderlyingProduct_SettlementReport.csv
# ftp://ftp.cmegroup.com/pub/settle/cbt.settle.20190906.s.txt
