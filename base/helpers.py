# from .models import Company
import datetime
def year_choices():
    return [(r,r) for r in range(1984, datetime.date.today().year+1)]

def current_year():
    return datetime.date.today().year
years = year_choices()


# def show_companies() : 
#     company_list = Company.objects.values_list()
#     name_list = [] 
#     for nm in company_list : 
#         name_list.append(nm) 
#     print(name_list)
#     return tuple((nm ,nm) for nm in name_list)