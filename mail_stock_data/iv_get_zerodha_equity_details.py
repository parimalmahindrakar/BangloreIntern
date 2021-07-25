from datetime import datetime  # 1
import requests  # 2
from bs4 import BeautifulSoup as bs  # 3
import calendar  # 4
from dateutil.relativedelta import relativedelta  # 5


def get_zerodha_equity_details(stock_name):

    url = "https://zerodha.com/margin-calculator/Futures/"
    resp = requests.get(url)
    soup = bs(resp.content, 'html.parser')

    def seven_day_bofore_last_thursday_date():
        today = datetime.today()
        this_year = int(today.strftime("%Y"))
        this_month = int(today.strftime("%m"))
        this_month_calendar = calendar.monthcalendar(this_year, this_month) # Calender as nested arrey
        last_thurs_date = this_month_calendar[4][3] if this_month_calendar[4][3] != 0 else this_month_calendar[3][3] 
        # print(last_thurs_date)
        return ( last_thurs_date - 7 )  # 7 day Before

    today_date = int(datetime.today().strftime("%d"))

    this_month = None
    next_month = None

    if today_date < seven_day_bofore_last_thursday_date():
        this_month = datetime.today().strftime("%B")[:3].upper()
        next_month = (datetime.today()+relativedelta(months=1)).strftime("%B")[:3].upper()
        print("[ Zerodha ]", this_month, next_month)

    else:
        # this month >became> next month
        this_month = (datetime.today()+relativedelta(months=1)
                      ).strftime("%B")[:3].upper()
        # next month >became> 2nd next month
        next_month = (datetime.today()+relativedelta(months=2)
                      ).strftime("%B")[:3].upper()
        print("[ Zerodha ]", this_month, next_month)

    equity_datails = []

    # Equity Details for This Month
    try:
        for tr in soup.find_all('tr'):
            row_text = tr.text
            row_text = row_text.split()
            if len(row_text) > 10 : # valid row to scrap
                if ( row_text[0] == stock_name ) and ( this_month in row_text[1] ) : # This Month
                    #print(row_text)
                    temp_list = []
                    temp_list.append(row_text[4])  # lot
                    temp_list.append(row_text[7])  # mrgn
                    equity_datails.append(temp_list)
                    break
    except IndexError:
        print(
            f"!  This Stock's Data for 1st Month:({this_month}) is Not Available in Zerodha Equity Futures ~ Error!")
        pass
    
    if len(equity_datails) == 0 :
        print( f"! We couldn't able to find {stock_name} Stock's Data for 1st Month of:({this_month})")
        return equity_datails

    # Equity Details for Next Month
    try:
        for tr in soup.find_all('tr'):
            row_text = tr.text
            row_text = row_text.split()
            if len(row_text) > 10 : # valid row to scrap
                if ( row_text[0] == stock_name ) and ( next_month in row_text[1] ) : # Next Month
                    #print(row_text)
                    temp_list = []
                    temp_list.append(row_text[4])  # lot
                    temp_list.append(row_text[7])  # mrgn
                    equity_datails.append(temp_list)
                    break
    except IndexError:
        print( f"!  This Stock's Data for 2nd Month:({next_month}) is Not Available in Zerodha Equity Futures ~ Error!")
        pass

    #print(f"   {len(equity_datails)} equity_data : ",this_month,'-to-', next_month, equity_datails)

    return equity_datails


#resp = get_zerodha_equity_details('ACC')
