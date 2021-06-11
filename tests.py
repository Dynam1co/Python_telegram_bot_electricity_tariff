import requests
import conf_management as Conf
import pytest
from bs4 import BeautifulSoup
from report import Report
import scrap as scp


def test_have_connection():
    resp = requests.get('https://google.es')
    
    assert resp.status_code == 200


def test_tariff_url_runs():
    resp = requests.get(Conf.get_source())

    assert resp.status_code == 200


def test_parse_content():
    file1 = open("response.txt","r", encoding="utf-8")

    text = file1.read()

    file1.close()

    if text != '':
        soup = BeautifulSoup(text, 'lxml')

    assert soup.is_empty_element == False

    if soup:
        price_text, price = scp.get_now(soup)
        mid_price_text, mid_price, mid_date_txt = scp.get_mean(soup, "inner_block gauge_day")
        low_price_text, low_price, low_date_txt = scp.get_low_hight(soup,"inner_block gauge_low")
        hight_price_text, hight_price, hight_date_txt = scp.get_low_hight(soup,"inner_block gauge_hight")

        assert price_text == 'Precio a las 18:26'
        assert price == '0.23436 €/kWh'
        assert mid_price_text == 'Precio medio del día'
        assert mid_price == '0.16179 €'
        assert mid_date_txt == '11 del 6 de 2021'
        assert low_price_text == 'Precio más bajo del día'
        assert low_price == ' 0.09614 €/kWh '
        assert low_date_txt == '04h - 05h'
        assert hight_price_text == 'Precio más alto del día'
        assert hight_price == ' 0.24423 €/kWh '
        assert hight_date_txt == '20h - 21h'

        my_day = Report(price_text, price, 
            mid_price_text, mid_price, mid_date_txt,
            low_price_text, low_price, low_date_txt, 
            hight_price_text, hight_price, hight_date_txt)

        my_day.fill_price_list(soup)

        assert len(my_day.breakdown) == 24
