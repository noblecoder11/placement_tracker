from django.db import connection
from collections import namedtuple
import datetime
def year_choices():
    return [(r,r) for r in range(2010, datetime.date.today().year+5)]

def current_year():
    return datetime.date.today().year
years = year_choices()
