from dataclasses import dataclass, field
from typing import List
from rate import Rate
import conf_management as ConfMgt


@dataclass
class Report:
    now_price_text: str
    now_price: str

    mid_price_text: str
    mid_price: str
    mid_date_txt: str

    low_price_text: str
    low_price: str
    low_date_txt: str

    hight_price_text: str
    hight_price: str
    hight_date_txt: str

    breakdown: list[Rate] = field(default_factory=list)

    def fill_price_list(self, soup):
        div_table = soup.find(id='hour_prices')

        for child in div_table.children:
            if child.name == 'div':
                if child.attrs['class'][0] == 'col-xs-9':
                    txt_hour = ''
                    txt_price = ''

                    for child2 in child.children:
                        if child2.name == 'span':
                            if child2.attrs['itemprop'] == 'description':
                                txt_hour = child2.next
                            elif child2.attrs['itemprop'] == 'price':
                                txt_price = child2.next

                            if txt_hour != '' and txt_price != '':
                                my_rate = Rate(txt_hour, txt_price)
                                my_rate.set_fl_price()
                                my_rate.set_level()

                                self.breakdown.append(my_rate)

    
    def prepare_message(self) -> str:
        red_circle = ConfMgt.get_red_circle()
        green_circle = ConfMgt.get_green_circle()

        message = f'Precio de la luz {self.mid_date_txt}\n\n'

        message += f'{self.now_price_text} {self.now_price}\n'
        message += f'{self.mid_price_text} {self.mid_price}\n'
        message += f'{self.low_price_text} {self.low_date_txt} {self.low_price}{green_circle}\n'
        message += f'{self.hight_price_text} {self.hight_date_txt} {self.hight_price}{red_circle}\n'

        message += '\nPrecio del kwh de luz por horas:\n\n'

        for rate in self.breakdown:
            message += f'{rate.hour_range} {rate.price}{rate.level}\n'

        return message