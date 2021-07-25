import shlex  # 1
import subprocess  # 2
import json  # 3
import ast
import requests
# from firebase_firestore import db
from update_nseappid import get_nseappid_updated

 
def get_nse_records(stock_name):

    try:
        # nseappid =  db.collection('IIFL').document('MailDashboard').get().to_dict()['nseappid']
        # print(nseappid)
        file = open("nseappid.txt", 'r')
        nseappid = file.readline()        
        stock_name = stock_name.replace('&', '%26')

        cmd = """curl 'https://www.nseindia.com/api/option-chain-equities?symbol="""+stock_name+"""' \
        -H 'authority: www.nseindia.com' \
        -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36' \
        -H 'dnt: 1' \
        -H 'accept: */*' \
        -H 'sec-fetch-site: same-origin' \
        -H 'sec-fetch-mode: cors' \
        -H 'sec-fetch-dest: empty' \
        -H 'referer: https://www.nseindia.com/get-quotes/derivatives?symbol="""+stock_name+"""' \
        -H 'accept-language: en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7' \
        -H 'cookie: nseQuoteSymbols=[{"symbol":"""+stock_name+""","identifier":null,"type":"equity"}]; nsit=YWOv35B8z1idWdohTXjUafZ6; nseappid="""+nseappid+"""; ' \
        --compressed"""


        args = shlex.split(cmd)
        process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        result = ast.literal_eval(stdout.decode("utf-8"))
        return result['records']

    except SyntaxError:
        print("SyntaxError : Occurred")
        # Update nseappid
        get_nseappid_updated()
        re_data = get_nse_records(stock_name)
        return re_data
        #Update NSEAPIID

    except KeyError:
        print("Raising KeyError:")
        raise KeyError


# print(get_nse_records("ADANIPOWER"))