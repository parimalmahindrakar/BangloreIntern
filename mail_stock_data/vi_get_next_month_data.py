def get_next_month_data(stock_name, records, call_strike_prices, put_strike_prices, exp_dates, equity_data, live_price):

    # Next Month
    nm_lot_size = equity_data[1][0]
    nm_margin = equity_data[1][1]

    resp = {
        'nm_c1_bid': None, 'nm_c1_prt': None, 'nm_c2_bid': None, 'nm_c2_prt': None, 'nm_c3_bid': None, 'nm_c3_prt': None, 'nm_c4_bid': None, 'nm_c4_prt': None,
        'nm_p1_bid': None, 'nm_p1_prt': None, 'nm_p2_bid': None, 'nm_p3_prt': None, 'nm_p3_bid': None, 'nm_p3_prt': None, 'nm_p4_bid': None, 'nm_p4_prt': None,
    }

    # Next Month Call

    # [ 1 ]
    try:
        strike_price = call_strike_prices[0]
        for data in records['data']:
            if data['strikePrice'] == strike_price and data['expiryDate'] == exp_dates[1]:
                resp['nm_c1_bid'] = round(
                    float(data['CE']['bidprice']) * float(nm_lot_size) * 100/float(nm_margin), 1)
                resp['nm_c1_prt'] = round(
                    (float(data['CE']['bidprice']) / float(live_price)) * 100, 1)

    except (IndexError, KeyError):
        resp['nm_c1_bid'] = 0
        resp['nm_c1_prt'] = 0

    # [ 2 ]
    try:
        strike_price = call_strike_prices[1]
        for data in records['data']:
            if data['strikePrice'] == strike_price and data['expiryDate'] == exp_dates[1]:
                resp['nm_c2_bid'] = round(
                    float(data['CE']['bidprice']) * float(nm_lot_size) * 100/float(nm_margin), 1)
                resp['nm_c2_prt'] = round(
                    (float(data['CE']['bidprice']) / float(live_price)) * 100, 1)

    except (IndexError, KeyError):
        resp['nm_c2_bid'] = 0
        resp['nm_c2_prt'] = 0

    # [ 3 ]
    try:
        strike_price = call_strike_prices[2]
        for data in records['data']:
            if data['strikePrice'] == strike_price and data['expiryDate'] == exp_dates[1]:
                resp['nm_c3_bid'] = round(
                    float(data['CE']['bidprice']) * float(nm_lot_size) * 100/float(nm_margin), 1)
                resp['nm_c3_prt'] = round(
                    (float(data['CE']['bidprice']) / float(live_price)) * 100, 1)

    except (IndexError, KeyError):
        resp['nm_c3_bid'] = 0
        resp['nm_c3_prt'] = 0  # Next Month Call

    # [ 4 ]
    try:
        strike_price = call_strike_prices[3]
        for data in records['data']:
            if data['strikePrice'] == strike_price and data['expiryDate'] == exp_dates[1]:
                resp['nm_c4_bid'] = round(
                    float(data['CE']['bidprice']) * float(nm_lot_size) * 100/float(nm_margin), 1)
                resp['nm_c4_prt'] = round(
                    (float(data['CE']['bidprice']) / float(live_price)) * 100, 1)

    except (IndexError, KeyError):
        resp['nm_c4_bid'] = 0
        resp['nm_c4_prt'] = 0

    # Next Month Put

    # [ 1 ]
    try:
        strike_price = put_strike_prices[-1]
        for data in records['data']:
            if data['strikePrice'] == strike_price and data['expiryDate'] == exp_dates[1]:
                resp['nm_p1_bid'] = round(
                    float(data['PE']['bidprice']) * float(nm_lot_size) * 100/float(nm_margin), 1)
                resp['nm_p1_prt'] = round(
                    (float(data['PE']['bidprice']) / float(live_price)) * 100, 1)

    except (IndexError, KeyError):
        resp['nm_p1_bid'] = 0
        resp['nm_p1_prt'] = 0

    # [ 2 ]
    try:
        strike_price = put_strike_prices[-2]
        for data in records['data']:
            if data['strikePrice'] == strike_price and data['expiryDate'] == exp_dates[1]:
                resp['nm_p2_bid'] = round(
                    float(data['PE']['bidprice']) * float(nm_lot_size) * 100/float(nm_margin), 1)
                resp['nm_p2_prt'] = round(
                    (float(data['PE']['bidprice']) / float(live_price)) * 100, 1)

    except (IndexError, KeyError):
        resp['nm_p2_bid'] = 0
        resp['nm_p2_prt'] = 0

    # [ 3 ]
    try:
        strike_price = put_strike_prices[-3]
        for data in records['data']:
            if data['strikePrice'] == strike_price and data['expiryDate'] == exp_dates[1]:
                resp['nm_p3_bid'] = round(
                    float(data['PE']['bidprice']) * float(nm_lot_size) * 100/float(nm_margin), 1)
                resp['nm_p3_prt'] = round(
                    (float(data['PE']['bidprice']) / float(live_price)) * 100, 1)

    except (IndexError, KeyError):
        resp['nm_p3_bid'] = 0
        resp['nm_p3_prt'] = 0

    # [ 4 ]
    try:
        strike_price = put_strike_prices[-4]
        for data in records['data']:
            if data['strikePrice'] == strike_price and data['expiryDate'] == exp_dates[1]:
                resp['nm_p4_bid'] = round(
                    float(data['PE']['bidprice']) * float(nm_lot_size) * 100/float(nm_margin), 1)
                resp['nm_p4_prt'] =  round(
                    (float(data['PE']['bidprice']) / float(live_price)) * 100, 1)

    except (IndexError, KeyError):
        resp['nm_p4_bid'] = 0
        resp['nm_p4_prt'] = 0

    return resp
