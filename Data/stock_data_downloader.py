from selenium import webdriver
from time import sleep
import os

PATH = "C:\Program Files (x86)\chromedriver.exe"
download_directory = r"C:\Users\Kamil\OneDrive\Python projects\Stock-visualisations\Data\Daily_data"
stock_list = ['ACP', 'ALE', 'ALR', 'CCC', 'CDR', 'CPS', 'DNP', 'JSW', 'KGH', 'LPP', 'LTS',
              'MRC', 'OPL', 'PEO', 'PGE', 'PGN', 'PKN', 'PKO', 'PZU', 'SAN', 'TPE']

# full url: https://stooq.pl/q/d/l/?s=cdr&i=d for CDR
url_pt1 = "https://stooq.pl/q/d/l/?s="
url_pt2 = "&i=d"

# change the downloaded files directory
options = webdriver.ChromeOptions()
prefs = {"download.default_directory": download_directory}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(executable_path=PATH, options=options)

# remove old files in the directory
for filename in os.listdir(download_directory):
    if filename[-3:] == 'csv':
        os.remove(os.path.join(download_directory, filename))

# download files
for stock in stock_list:
    url = url_pt1 + stock.lower() + url_pt2
    driver.get(url)

sleep(5)
driver.quit()
