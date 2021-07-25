import shlex
import subprocess
import json
import ast
import time
import requests
# import getid
import itertools
import csv
import datetime
import os
from pyexcel.cookbook import merge_all_to_a_book
import glob


os.system("mkdir csv_files")


class NSE_Records:

    nseappid = open("nseappid.txt",'r').readline()
    all_records = {}
    def __init__(self,stock_name):
        self.stock_name = stock_name.replace('&', '%26')

    def get_corresponding_records(self):
        cmd = """curl 'https://www.nseindia.com/api/option-chain-equities?symbol=""" + self.stock_name + """' \
                -H 'authority: www.nseindia.com' \
                -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36' \
                -H 'dnt: 1' \
                -H 'accept: */*' \
                -H 'sec-fetch-site: same-origin' \
                -H 'sec-fetch-mode: cors' \
                -H 'sec-fetch-dest: empty' \
                -H 'referer: https://www.nseindia.com/get-quotes/derivatives?symbol=""" + self.stock_name + """' \
                -H 'accept-language: en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7' \
                -H 'cookie: nseQuoteSymbols=[{"symbol":""" + self.stock_name + ""","identifier":null,"type":"equity"}]; nsit=YWOv35B8z1idWdohTXjUafZ6; nseappid=""" + NSE_Records.nseappid + """; ' \
                --compressed"""
        # print(cmd)
        args = shlex.split(cmd)
        process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        result = ast.literal_eval(stdout.decode("utf-8"))
        try:
            NSE_Records.all_records.update({self.stock_name: {
                "expiryDates" : result['records']['expiryDates'],
                "strikePrices" : result['records']['strikePrices'],
                "underlyingValue":result['records']['underlyingValue'],
                "data": [i for i in result['records']['data'] if i['expiryDate'] == '25-Feb-2021']
            }})
        except KeyError as e:
            pass

    def get_all_records(self):
        return NSE_Records.all_records

    def get_strike_prices(self):
        return  self.get_all_records()[self.stock_name]['strikePrices']

    def get_steps_diff_btw_strike_prices(self):
        diff = []
        data = self.get_strike_prices()
        tobe_diff = self.get_all_records()[self.stock_name]['strikePrices'][0]
        for i in range(len(data)):
            try:
                diff.append(data[i+1]-tobe_diff)
            except:
                pass
        return diff[:6]

    def get_underlying_value(self):
        return self.get_all_records()[self.stock_name]['underlyingValue']

    def get_live_strike(self):
        underlying_value = self.get_underlying_value()
        live_strike = [round((underlying_value-i),2) for i in self.get_strike_prices()]
        return live_strike

    def get_strike_prcnt_live(self):
        strike_prcnt_live = [ round(i/self.get_underlying_value(),2) for i in self.get_live_strike()]
        return strike_prcnt_live

    def get_ask_price(self):
        data = [i for i in self.get_all_records()[self.stock_name]['data']]
        askPrice = []
        for i in data:
            try :
                askPrice.append(i['CE']['askPrice'])
            except:
                pass
        return askPrice

    def get_bid_price(self):
        data = [i for i in self.get_all_records()[self.stock_name]['data']]
        bidprice = []
        for i in data:
            try :
                bidprice.append(i['CE']['bidprice'])
            except:
                pass
        return bidprice

    def get_ask_arbitrage(self):
        live_strike = self.get_live_strike()
        ask_price = self.get_ask_price()
        aks_arbitrage = []
        ask_arbitrage_rounded = []
        for i,j in zip(live_strike,ask_price):
            aks_arbitrage.append(round(i, 2) - round(j, 2))
        for i in aks_arbitrage:
            ask_arbitrage_rounded.append(round(i,2))
        return ask_arbitrage_rounded

    def get_bid_arbitrage(self):
        live_strike = self.get_live_strike()
        bid_price = self.get_bid_price()
        bid_arbitrage = []
        bid_arbitrage_new = []
        for i,j in zip(live_strike,bid_price):
            bid_arbitrage.append(round(i,2)-round(j,2))
        for i in bid_arbitrage:
            bid_arbitrage_new.append(round(i, 2))
        return bid_arbitrage_new
            

    def get_n_step_difference(self,number):
        bid_arbitrage = self.get_bid_arbitrage()
        ask_arbitrage = self.get_ask_arbitrage()
        n_step_diff = []
        n_step_diff_round = []
        for i, j in zip(range(len(ask_arbitrage)), range(len(bid_arbitrage))):
            try:
                n_step_diff.append(round(bid_arbitrage[j + number],2) - round(ask_arbitrage[i],2))
            except:
                n_step_diff.append(0 - round(ask_arbitrage[i], 2))
        for i in n_step_diff:
            n_step_diff_round.append(round(i,2))
        return n_step_diff_round

    def get_n_step_arbitrage(self, num):
        n_step_arbitrage = []
        n_step_differences = self.get_n_step_difference(num)
        step_diff = self.get_steps_diff_btw_strike_prices()[num-1]
        for i in n_step_differences:
            n_step_arbitrage.append(round(i * 100/ step_diff,2))
        return n_step_arbitrage

        
        
        

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

# stock_names = ['ACC']

for stock_name in stock_names:
    record = NSE_Records(stock_name)
    try :
        record.get_corresponding_records()
        # strike_prices = record.get_strike_prices()
        # strike_live_prcnt = record.get_strike_prcnt_live()
        # bid_price = record.get_bid_price()
        # ask_price = record.get_ask_price()
        # bid_arbitrage = record.get_bid_arbitrage()
        # ask_arbitrage = record.get_ask_arbitrage()
        # steps = record.get_steps_diff_btw_strike_prices()
        # nstep_diff = {
        #     "step_1_diff": record.get_n_step_difference(1),
        #     "step_2_diff": record.get_n_step_difference(2),
        #     "step_3_diff": record.get_n_step_difference(3),
        #     "step_4_diff": record.get_n_step_difference(4),
        #     "step_5_diff": record.get_n_step_difference(5),
        #     "step_6_diff": record.get_n_step_difference(6),
        # }
        # nstepp_arbitrage = {
        #     "step_1_arbitrage": record.get_n_step_arbitrage(1),
        #     "step_2_arbitrage": record.get_n_step_arbitrage(2),
        #     "step_3_arbitrage": record.get_n_step_arbitrage(3),
        #     "step_4_arbitrage": record.get_n_step_arbitrage(4),
        #     "step_5_arbitrage": record.get_n_step_arbitrage(5),
        #     "step_6_arbitrage": record.get_n_step_arbitrage(6),
        # }
        print(stock_name, "=> GOT DATA FROM NSE.")
        # data_lists = [
        #     stock_name, '''={''',
        #     "\n\t",'''"''', "steps",'''":''' + str(steps),''',''',
        #     "\n\t", '''"''', "strike_prices", '''":''' + str(strike_prices), ''',''',
        #     "\n\t",'''"''',"strike_live_prcnt", '''":'''+ str(strike_live_prcnt),''',''',
        #     "\n\t",'''"''', "bid_arbitrage",'''":''' + str(bid_arbitrage),''',''',
        #     "\n\t",'''"''', "ask_arbitrage",'''":''' + str(ask_arbitrage),''',''',
        #     "\n\t",'''"''', "nstep_diff",'''":''' + str(nstep_diff),''',''',
        #     "\n\t", '''"''', "nstepp_arbitrage", '''":''' + str(nstepp_arbitrage), ''',''',
        #     "\n\t",'''"''', "bid_price",'''":''' + str(bid_price),''',''',
        #     "\n\t",'''"''', "ask_price",'''":''' + str(ask_price),''',''','''\n}'''
        #     "\n\n\n\n\n"]

        # data = {}
        # data.update({"steps": steps})
        # data.update({"strike_prices": strike_prices})
        # data.update({"strike_live_prcnt": strike_live_prcnt})
        # data.update({"bid_arbitrage": bid_arbitrage})
        # data.update({"ask_arbitrage": ask_arbitrage})
        # data.update({"nstep_diff": nstep_diff})
        # data.update({"nstepp_arbitrage": nstepp_arbitrage})
        # data.update({"bid_price": bid_price})
        # data.update({"ask_price":ask_price})
        # datanew = {}

        # for i, j in data.items():
        #     if type(j) == list:
        #         datanew.update({i:j})
        #     if type(j) == dict:
        #         for k,l in j.items():
        #             datanew.update({k: l})
        
        # filename = "./csv_files/"+stock_name + ".csv"  
        # with open(filename, "w") as outfile:
        #     writer = csv.writer(outfile)
        #     writer.writerow(datanew.keys())
        #     writer.writerows(itertools.zip_longest(*datanew.values()))        

    except KeyError:
            print(stock_name , "=> DIDN'T GOT DATA FROM NSE." )
            continue

    except SystemError:
        print("Syntax error : [occured]")
        # getid.get_nseappid_updated()
# merge_all_to_a_book(glob.glob("csv_files//*.csv"), "output.xlsx")
'''
[Updated nseappid] :  eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhcGkubnNlIiwiYXVkIjoiYXBpLm5zZSIsImlhdCI6MTYwNzQxMTE1MCwiZXhwIjoxNjA3NDE0NzUwfQ.M-wz1oVnc7VjRfzZRupZcOWuA6eVRGuKEfk6LFNjj2s
ACC => GOT DATA FROM NSE.
ADANIPOWER =>DIDN'T GOT DATA FROM NSE.
'''