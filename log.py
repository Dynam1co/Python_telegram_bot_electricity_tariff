from dataclasses import dataclass
from datetime import date

@dataclass
class Log:
    category: str
    text: str