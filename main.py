from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass, field, asdict
import time
from math import ceil
from urllib.parse import urljoin
import json
import csv

##########################################
# creating dataclasses from products

@dataclass
class bookInfo:
    id: int = field(init=False)
    name: str
    price: str
    url: str

    def __post_init__(self):
        getTime = ceil(time.time())
        self.id = getTime
        


##########################################
# scrapeBooksUrl function

def scrapeBooksUrl():
    base = "https://books.toscrape.com/"
    extend = ""
    url = urljoin(base, extend)

    #########################################
    # creating a list to store bookInfo object

    book_url_data_list = []
    page = 1
    while True:
        res = requests.get(url)

        if res.status_code == 200:
            html = res.text
            soup = BeautifulSoup(html, 'lxml')

            #######################################
            # scrape data

            books_li = soup.select('ol.row li')
            for li in books_li:
                product_name = li.article.h3.a.string
                product_url = li.article.h3.a['href']
                price_tag = li.article.select_one('div.product_price p.price_color')
                product_price = price_tag.string

                bookInfoObj = bookInfo(
                    name = product_name,
                    price = product_price,
                    url = product_url
                )

                book_url_data_list.append(bookInfoObj)

            try:
                next_btn = soup.select_one('li.next')
                extend = next_btn.a['href']
                page += 1
            except:
                break
            url = urljoin(base, extend)
            print(f"Url No: {page}")
        else:
            base_2 = "https://books.toscrape.com/catalogue/"
            url = urljoin(base_2, extend)

    return (book_url_data_list, page)



url_list, total_page = scrapeBooksUrl()

print(f"\n\nPrinting Report: \n\t Total num of page scraped: {total_page}\n\t Total num of data: {len(url_list)}\n\t Glance of last data: {url_list[-1].__dict__}\n\n")



##################################################
# Writing files to csv

with open('book_url_data.csv', mode='a', encoding='utf-8') as csv_file:
    headers = ['id', 'name', 'price', 'url']
    writer = csv.DictWriter(csv_file, fieldnames= headers, dialect='excel')
    writer.writeheader()
    for info in url_list:
        data_dict = {
            'id': info.id,
            'name': info.name,
            'price': info.price,
            'url': info.url
        }
        writer.writerow(data_dict)
    
    print('"book_url_data.csv" file is saved in the directory.....')