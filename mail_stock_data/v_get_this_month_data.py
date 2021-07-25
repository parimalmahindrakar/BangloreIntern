 

def get_this_month_data(stock_name, records, call_strike_prices, put_strike_prices, exp_dates, equity_data, live_price):

    # This Month
    tm_lot_size = equity_data[0][0]
    tm_margin = equity_data[0][1]

    resp = {
        'tm_c1_bid': None, 'tm_c1_prt': None, 'tm_c2_bid': None, 'tm_c2_prt': None, 'tm_c3_bid': None, 'tm_c3_prt': None, 'tm_c4_bid': None, 'tm_c4_prt': None,
        'tm_p1_bid': None, 'tm_p1_prt': None, 'tm_p2_bid': None, 'tm_p2_prt': None, 'tm_p3_bid': None, 'tm_p3_prt': None, 'tm_p4_bid': None, 'tm_p4_prt': None,
    }

    try:
        strike_price = call_strike_prices[0] # forward indexing
        for data in records['data']:
            if data['strikePrice'] == strike_price and data['expiryDate'] == exp_dates[0]:
                resp['tm_c1_bid'] = round(float(data['CE']['bidprice']) * float(tm_lot_size) * 100/float(tm_margin), 1)
                resp['tm_c1_prt'] = round((float(data['CE']['bidprice']) / float(live_price)) * 100, 1)

    except (IndexError, KeyError):
        resp['tm_c1_bid'] = 0
        resp['tm_c1_prt'] = 0

    # [ 2 ]
    try:
        strike_price = call_strike_prices[1] # forward indexing
        for data in records['data']:
            if data['strikePrice'] == strike_price and data['expiryDate'] == exp_dates[0]:
                resp['tm_c2_bid'] = round(float(data['CE']['bidprice']) * float(tm_lot_size) * 100/float(tm_margin), 1)
                resp['tm_c2_prt'] = round((float(data['CE']['bidprice']) / float(live_price)) * 100, 1)

    except (IndexError, KeyError):
        resp['tm_c2_bid'] = 0
        resp['tm_c2_prt'] = 0

    # [ 3 ]
    try:
        strike_price = call_strike_prices[2] # forward indexing
        for data in records['data']:
            if data['strikePrice'] == strike_price and data['expiryDate'] == exp_dates[0]:
                resp['tm_c3_bid'] = round(
                    float(data['CE']['bidprice']) * float(tm_lot_size) * 100/float(tm_margin), 1)
                resp['tm_c3_prt'] = round(
                    (float(data['CE']['bidprice']) / float(live_price)) * 100, 1)

    except (IndexError, KeyError):
        resp['tm_c3_bid'] = 0
        resp['tm_c3_prt'] = 0

    # [ 4 ]
    try:
        strike_price = call_strike_prices[3] # forward indexing
        for data in records['data']:
            if data['strikePrice'] == strike_price and data['expiryDate'] == exp_dates[0]:
                resp['tm_c4_bid'] = round(
                    float(data['CE']['bidprice']) * float(tm_lot_size) * 100/float(tm_margin), 1)
                resp['tm_c4_prt'] = round(
                    (float(data['CE']['bidprice']) / float(live_price)) * 100, 1)

    except (IndexError, KeyError):
        resp['tm_c4_bid'] = 0
        resp['tm_c4_prt'] = 0

    # This Month Put

    # [ 1 ]
    try:
        strike_price = put_strike_prices[-1] # backword indexing
        for data in records['data']:
            if data['strikePrice'] == strike_price and data['expiryDate'] == exp_dates[0]:
                resp['tm_p1_bid'] = round(float(data['PE']['bidprice']) * float(tm_lot_size) * 100/float(tm_margin), 1)
                resp['tm_p1_prt'] = round((float(data['PE']['bidprice']) / float(live_price)) * 100, 1)

    except (IndexError, KeyError):
        resp['tm_p1_bid'] = 0
        resp['tm_p1_prt'] = 0

    # [ 2 ]
    try:
        strike_price = put_strike_prices[-2] # backword indexing
        for data in records['data']:
            if data['strikePrice'] == strike_price and data['expiryDate'] == exp_dates[0]:
                resp['tm_p2_bid'] = round(
                    float(data['PE']['bidprice']) * float(tm_lot_size) * 100/float(tm_margin), 1)
                resp['tm_p2_prt'] = round(
                    (float(data['PE']['bidprice']) / float(live_price)) * 100, 1)

    except (IndexError, KeyError):
        resp['tm_p2_bid'] = 0
        resp['tm_p2_prt'] = 0

    # [ 3 ]
    try:
        strike_price = put_strike_prices[-3] # backword indexing
        for data in records['data']:
            if data['strikePrice'] == strike_price and data['expiryDate'] == exp_dates[0]:
                resp['tm_p3_bid'] = round(
                    float(data['PE']['bidprice']) * float(tm_lot_size) * 100/float(tm_margin), 1)
                resp['tm_p3_prt'] = round(
                    (float(data['PE']['bidprice']) / float(live_price)) * 100, 1)

    except (IndexError, KeyError):
        resp['tm_p3_bid'] = 0
        resp['tm_p3_prt'] = 0

    # [ 4 ]
    try:
        strike_price = put_strike_prices[-4] # backword indexing
        for data in records['data']:
            if data['strikePrice'] == strike_price and data['expiryDate'] == exp_dates[0]:
                resp['tm_p4_bid'] = round(
                    float(data['PE']['bidprice']) * float(tm_lot_size) * 100/float(tm_margin), 1)
                resp['tm_p4_prt'] = round(
                    (float(data['PE']['bidprice']) / float(live_price)) * 100, 1)

    except (IndexError, KeyError):
        resp['tm_p4_bid'] = 0
        resp['tm_p4_prt'] = 0

    return resp
