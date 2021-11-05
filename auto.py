import requests
from lxml import html as h, etree
import pandas as pd
import numpy as np


def format_data(inp):
    return str(inp.replace('\xa0', '')
               .replace('км', '')
               .replace('₽', '')
               )


def load_data(url):
    all_list = []
    r = requests.get(url)
    r.encoding = 'utf-8'
    tree = h.fromstring(r.text)
    main_selector = "//div[@class='ListingItem__main']"
    all_autos = tree.xpath(main_selector)
    print('Найдено записей ' + str(len(all_autos)))
    for i in range(len(all_autos)):
        local_tree = h.fromstring(etree.tostring(all_autos[i]).decode('utf-8'))

        price_selector = "//a[@class='Link ListingItemPrice__link']/span/text()"
        price_alter_selector = "//div[@class='ListingItemPrice__content']/text()"
        price = []
        if len(local_tree.xpath(price_selector)):
            price = local_tree.xpath(price_selector)[0]
        if price == [] and len(local_tree.xpath(price_alter_selector)) > 0:
            price = local_tree.xpath(price_alter_selector)[0]
        try:
            price = int(format_data(price))
        except:
            price = 0

        mileage_selector = "//div[@class='ListingItem__kmAge']/text()"
        mileage = local_tree.xpath(mileage_selector)[0]
        try:
            mileage = int(format_data(mileage))
        except:
            mileage = 0
        year_selector = "//div[@class='ListingItem__year']/text()"
        year = local_tree.xpath(year_selector)[0]
        try:
            year = int(format_data(year))
        except:
            year = 0
        link_selector = "//a[@class='Link ListingItemTitle__link']/@href"
        link = local_tree.xpath(link_selector)[0]
        modelname_selector = "//a[@class='Link ListingItemTitle__link']/text()"
        modelname = local_tree.xpath(modelname_selector)[0]
        city_selector = "//span[@class='MetroListPlace__regionName MetroListPlace_nbsp']/text()"
        try:
            city = ' '.join(local_tree.xpath(city_selector))
        except IndexError:
            city = ''
        all_list.append([modelname, link, year, price, mileage, city])

    data = np.array(all_list)
    pd.set_option("display.max.columns", None)
    df = pd.DataFrame(data, columns=['modelname', 'link', 'year', 'price', 'mileage', 'city'])
    df.year = pd.to_numeric(df.year)
    df.mileage = pd.to_numeric(df.mileage)
    df.price = pd.to_numeric(df.price)
    return df
