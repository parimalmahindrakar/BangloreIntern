# dependencies and libraries
import time  # 1
from pandas import pandas as pd  # 2
from datetime import datetime  # 3

# Files
from ii_check_internet_connection import internet_connection
from iii_get_nse_records import get_nse_records
from iv_get_zerodha_equity_details import get_zerodha_equity_details
from v_get_this_month_data import get_this_month_data
from vi_get_next_month_data import get_next_month_data


# NSE has data/not?
at_least_one_data = False


def this_month(tm_strike_prices, live_price, records, exp_dates, equity_data):
    print("tm_strike_prices:",tm_strike_prices)

    for strike_price in tm_strike_prices:
        if live_price < strike_price:
            c_strt_ind = tm_strike_prices.index(strike_price) + 2  # ind of SP for CALL
            p_strt_ind = c_strt_ind - 2  # ind of SP for PUT
            print( "c_strt_ind : ", c_strt_ind)
            print("p_strt_ind : ", p_strt_ind)

            call_strike_prices = tm_strike_prices[
                c_strt_ind:
            ]  # list [c_strt_ind(i0), i1, i2, i3, .. ]
            print('call_strike_prices : ', call_strike_prices)
            put_strike_prices = tm_strike_prices[
                :p_strt_ind
            ]  # list [.., -i3, -i2, (-i1)p_strt_ind]
            print("put_strike_prices :",put_strike_prices)
            result_data = get_this_month_data(
                stock_name,
                records,
                call_strike_prices,
                put_strike_prices,
                exp_dates,
                equity_data,
                live_price,
            )
            return result_data
            break


def next_month(nm_strike_prices, live_price, records, exp_dates, equity_data):
    for strike_price in nm_strike_prices:
        if live_price < strike_price:

            c_strt_ind = nm_strike_prices.index(strike_price) + 2  # ind of SP for CALL
            p_strt_ind = c_strt_ind - 2  # ind of SP for PUT

            call_strike_prices = nm_strike_prices[
                c_strt_ind:
            ]  # list [c_strt_ind(i0), i1, i2, i3, .. ]
            put_strike_prices = nm_strike_prices[
                :p_strt_ind
            ]  # list [.., -i3, -i2, (-i1)p_strt_ind]

            result_data = get_next_month_data(
                stock_name,
                records,
                call_strike_prices,
                put_strike_prices,
                exp_dates,
                equity_data,
                live_price,
            )
            return result_data
            break


def main(stock_name):

    # Initial value of all data
    all_data = {
        "stock_name": None,
        "live_price": None,
        "tm_c1_bid": None,
        "tm_c2_bid": None,
        "tm_c3_bid": None,
        "tm_c4_bid": None,
        "tm_c1_prt": None,
        "tm_c2_prt": None,
        "tm_c3_prt": None,
        "tm_c4_prt": None,
        "tm_p1_bid": None,
        "tm_p2_bid": None,
        "tm_p3_bid": None,
        "tm_p4_bid": None,
        "tm_p1_prt": None,
        "tm_p2_prt": None,
        "tm_p3_prt": None,
        "tm_p4_prt": None,
        "nm_c1_bid": None,
        "nm_c2_bid": None,
        "nm_c3_bid": None,
        "nm_c4_bid": None,
        "nm_c1_prt": None,
        "nm_c2_prt": None,
        "nm_c3_prt": None,
        "nm_c4_prt": None,
        "nm_p1_bid": None,
        "nm_p2_bid": None,
        "nm_p3_bid": None,
        "nm_p4_bid": None,
        "nm_p1_prt": None,
        "nm_p2_prt": None,
        "nm_p3_prt": None,
        "nm_p4_prt": None,
    }

    try:
        # Returns JSON response from NSE_India
        records = get_nse_records(stock_name)
        # print(records)
        global at_least_one_data
        at_least_one_data = True
    except Exception as e:
        # print(e)
        print(
            "!  Some Error is coming(/No Data) from NSE website for this stock  ~  Error!"
        )

        all_data["stock_name"] = stock_name
        return all_data  # NSE has no data for this Stock

    live_price = records["underlyingValue"]
    all_data["stock_name"] = stock_name  # stock_name_updated
    all_data["live_price"] = live_price  # live_price_updated

    exp_dates = []  # ALl exp stock_namedates of the Stock in main_JSON_data

    for date in records["expiryDates"]:
        exp_dates.append(date)

        # Get Equity Data
    equity_data = get_zerodha_equity_details(stock_name)  # This Month , Next Month
    print("equitiy data :", equity_data)
    print(
        f"  >>  {len(exp_dates)} exp_dates : ",
        exp_dates,
        f"   >>  {len(equity_data)} equity_data : ",
        equity_data,
    )

    if len(equity_data) < 1 or len(exp_dates) < 1:
        pass  # return null values instead of skipping this stock << fix this.

    # Some times DATA only available for One month in (NSC Website | ZERODHA Website, when we shift one month * 7 days basis)
    elif len(equity_data) < 2 or len(exp_dates) < 2:

        tm_strike_prices = []  # All Strike Prices for Only This Month

        for data in records["data"]:
            if data["expiryDate"] == exp_dates[0]:
                tm_strike_prices.append(data["strikePrice"])

        res_data = this_month(
            tm_strike_prices, live_price, records, exp_dates, equity_data
        )
        all_data.update(res_data)

    else:  # When DATA available for more than One month (2):

        tm_strike_prices = []
        nm_strike_prices = []
        for data in records["data"]:
            if data["expiryDate"] == exp_dates[0]:  # TM
                tm_strike_prices.append(data["strikePrice"])
            if data["expiryDate"] == exp_dates[1]:  # NM
                nm_strike_prices.append(data["strikePrice"])
        # This Month
        tm_res_data = this_month(
            tm_strike_prices, live_price, records, exp_dates, equity_data
        )
        if tm_res_data:
            all_data.update(tm_res_data)
        else:
            all_data.update(
                {
                    "tm_c1_bid": None,
                    "tm_c1_prt": None,
                    "tm_c2_bid": None,
                    "tm_c2_prt": None,
                    "tm_c3_bid": None,
                    "tm_c3_prt": None,
                    "tm_c4_bid": None,
                    "tm_c4_prt": None,
                    "tm_p1_bid": None,
                    "tm_p1_prt": None,
                    "tm_p2_bid": None,
                    "tm_p2_prt": None,
                    "tm_p3_bid": None,
                    "tm_p3_prt": None,
                    "tm_p4_bid": None,
                    "tm_p4_prt": None,
                }
            )

        # Next Month
        nm_res_data = next_month(
            nm_strike_prices, live_price, records, exp_dates, equity_data
        )
        if nm_res_data:
            all_data.update(nm_res_data)
        else:
            all_data.update(
                {
                    "nm_c1_bid": None,
                    "nm_c1_prt": None,
                    "nm_c2_bid": None,
                    "nm_c2_prt": None,
                    "nm_c3_bid": None,
                    "nm_c3_prt": None,
                    "nm_c4_bid": None,
                    "nm_c4_prt": None,
                    "nm_p1_bid": None,
                    "nm_p1_prt": None,
                    "nm_p2_bid": None,
                    "nm_p3_prt": None,
                    "nm_p3_bid": None,
                    "nm_p3_prt": None,
                    "nm_p4_bid": None,
                    "nm_p4_prt": None,
                }
            )

    return all_data


if __name__ == "__main__":

    start_time = time.time()
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n\n")
    print(f"{datetime.today().strftime('~ %d/%h/%Y > %a > %Hh:%Mm')}")
    print("__________________________________")

    stock_names = ['ACC', 'ADANIENT', 'ADANIPORTS', 'ADANIPOWER', 'AMARAJABAT', 'AMBUJACEM',
                        'APOLLOHOSP', 'APOLLOTYRE', 'ASHOKLEY', 'ASIANPAINT', 'AUROPHARMA', 'AXISBANK',
                        'BAJAJ-AUTO', 'BAJAJFINSV', 'BAJFINANCE', 'BALKRISIND', 'BANDHANBNK', 'BANKBARODA',
                        'BATAINDIA', 'BEL', 'BERGEPAINT', 'BHARATFORG', 'BHARTIARTL', 'BHEL', 'BIOCON',
                        'BOSCHLTD', 'BPCL', 'BRITANNIA', 'CADILAHC', 'CANBK', 'CENTURYTEX', 'CESC',
                        'CHOLAFIN', 'CIPLA', 'COALINDIA', 'COLPAL', 'CONCOR', 'CUMMINSIND', 'DABUR',
                        'DIVISLAB', 'DLF', 'DRREDDY', 'EICHERMOT', 'EQUITAS', 'ESCORTS', 'EXIDEIND',
                        'FEDERALBNK', 'GAIL', 'GLENMARK', 'GMRINFRA', 'GODREJCP', 'GRASIM', 'HAVELLS',
                        'HCLTECH', 'HDFC', 'HDFCBANK', 'HDFCLIFE', 'HEROMOTOCO', 'HINDALCO', 'HINDPETRO',
                        'HINDUNILVR', 'IBULHSGFIN', 'ICICIBANK', 'ICICIPRULI', 'IDEA', 'IDFCFIRSTB', 'IGL',
                        'INDIGO', 'INDUSINDBK', 'INFRATEL', 'INFY', 'IOC', 'ITC', 'JINDALSTEL', 'JSWSTEEL',
                        'JUBLFOOD', 'JUSTDIAL', 'KOTAKBANK', 'L&TFH', 'LICHSGFIN', 'LT', 'LUPIN', 'M&M',
                        'M&MFIN', 'MANAPPURAM', 'MARICO', 'MARUTI', 'MCDOWELL-N', 'MFSL', 'MGL', 'MINDTREE',
                        'MOTHERSUMI', 'MRF', 'MUTHOOTFIN', 'NATIONALUM', 'NAUKRI', 'NCC', 'NESTLEIND',
                        'NIITTECH', 'NMDC', 'NTPC', 'OIL', 'ONGC', 'PAGEIND', 'PEL', 'PETRONET', 'PFC',
                        'PIDILITIND', 'PNB', 'POWERGRID', 'PVR', 'RAMCOCEM', 'RBLBANK', 'RECLTD', 'RELIANCE',
                        'SAIL', 'SBIN', 'SHREECEM', 'SIEMENS', 'SRF', 'SRTRANSFIN', 'SUNPHARMA', 'SUNTV',
                        'TATACHEM', 'TATACONSUM', 'TATAMOTORS', 'TATAPOWER', 'TATASTEEL', 'TCS', 'TECHM',
                        'TITAN', 'TORNTPHARM', 'TORNTPOWER', 'TVSMOTOR', 'UBL', 'UJJIVAN', 'ULTRACEMCO',
                        'UPL', 'VEDL', 'VOLTAS', 'WIPRO', 'YESBANK', 'ZEEL']
    # stock_names = ["ACC"]

    data = pd.DataFrame([])

    if internet_connection():
        for stock_name in stock_names:
            print("\n~  " + stock_name + "-")
            try:
                # main_fucn returns all data of given stock
                resp_data = main(stock_name)
                # New_row_of_next_stock_data
                new_data = pd.DataFrame(resp_data, index=[0])
                # Adding new data to main_data
                data = data.append(new_data, ignore_index=True)
                # print(data)
            except Exception as e:
                print(e, "  Error!")

        data.to_csv("x_stock_data.csv")
        print("\n# Finished in:", round(time.time() - start_time, 2), "Sec")

        # send_mail(at_least_one_data)
        print("Done :)")

    else:
        print("\n[ ERROR ] No Internet !\n")






