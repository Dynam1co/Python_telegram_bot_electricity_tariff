import requests
from bs4 import BeautifulSoup
import conf_management as ConfMgt
from report import Report


def get_data():
    try:
        r = requests.get(ConfMgt.get_source())

        if r:
            soup = BeautifulSoup(r.text, 'lxml')
    except:
        return None

    return soup


def get_now(soup):
    price_text = ''
    price = ''

    div_now = soup.find('div', class_="inner_block gauge_hour")

    for child in div_now.children:
        if child.name == 'h2':
            price_text = str(child.next).replace('\t', '')
            price_text = price_text.replace('\n', ' ')
        elif child.name == 'span':
            price = str(child.next).replace('\t', '')
            price = price.replace('\n', ' ')

    return price_text, price


def get_mean(soup, txtClass):
    price_text = ''
    price = ''
    date_text = ''

    div_mean = soup.find('div', class_="inner_block gauge_day")

    for child in div_mean:
        if child.name == 'h2':
            price_text = str(child.next).replace('\t', '')
            price_text = price_text.replace('\n', ' ')
        elif child.name == 'span':
            if child.attrs['class'][0] == 'main_text':
                price = str(child.next).replace('\t', '')
                price = price.replace('\n', ' ')
            elif child.attrs['class'][0] == 'sub_text':
                date_text = str(child.next).replace('\t', '')
                date_text = date_text.replace('\n', ' ')

    return price_text, price, date_text


def get_low_hight(soup, txtClass):
    price_text = ''
    price = ''
    date_text = ''

    div_low = soup.find('div', class_=txtClass)

    for child in div_low:
        if child.name == 'h2':
            price_text = str(child.next).replace('\t', '')
            price_text = price_text.replace('\n', ' ')
        elif child.name == 'span':
            if child.attrs['class'][0] == 'main_text':
                price = str(child.next).replace('\t', '')
                price = price.replace('\n', ' ')
            elif child.attrs['class'][0] == 'sub_text':
                for child2 in child.children:
                    if child2.name == 'div':
                        date_text = str(child2.next).replace('\t', '')
                        date_text = date_text.replace('\n', ' ')

    return price_text, date_text, price


def main():
    soup = get_data()

    if soup:
        price_text, price = get_now(soup)
        mid_price_text, mid_price, mid_date_txt = get_mean(soup, "inner_block gauge_day")
        low_price_text, low_price, low_date_txt = get_low_hight(soup,"inner_block gauge_low")
        hight_price_text, hight_price, hight_date_txt = get_low_hight(soup,"inner_block gauge_hight")

        my_day = Report(price_text, price, 
            mid_price_text, mid_price, mid_date_txt,
            low_price_text, low_price, low_date_txt, 
            hight_price_text, hight_price, hight_date_txt)

        my_day.fill_price_list(soup)

        return my_day