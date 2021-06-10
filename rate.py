from dataclasses import dataclass
from datetime import datetime
import conf_management as ConfMgt

@dataclass
class Rate:    
    hour_range: str
    price: str
    level: str = ConfMgt.get_green_circle()
    entry_date: datetime = datetime.now()
    fl_price: float = 0

    def set_fl_price(self):
        if len(self.price) == 0:            
            return

        pos = str(self.price).find(' ')        

        if pos == -1:
            return

        try:
            result = float(self.price[0:pos])
        except:
            result = 0

        self.fl_price = result

    def set_level(self):
        if self.fl_price > 0.15:
            self.level = ConfMgt.get_red_circle()