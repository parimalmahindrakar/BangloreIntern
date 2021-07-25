from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options  
import time

# from firebase_firestore import db


def get_nseappid_updated():
    # Options for Headless driver
    chrome_options = Options()  
    chrome_options.add_argument("--headless")   

    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36"
    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # open it, go to a website, and get results
    # driver Location
    driver = webdriver.Chrome(executable_path="./web_drivers/chromedriver", chrome_options=chrome_options)  #chrome_options
    # driver.execute_script("return navigator.userAgent")
    driver.get('http://www.nseindia.com/get-quotes/derivatives?symbol=SBIN')
    print("\n\n\n")
    print((driver.get_cookies()))
    print("\n\n\n")
    # print((driver.get_cookies()[-2]))

    nseappid = driver.get_cookies()[-2]['value']
    # db.collection('IIFL').document('MailDashboard').set({"nseappid": nseappid}, merge=True)
    print("[Updated nseappid] : ", nseappid)
    with open("nseappid.txt", 'w') as file:
        file.write(nseappid)

    # time.sleep(1)

    driver.quit()

get_nseappid_updated()
#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9 
#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhcGkubnNlIiwiYXVkIjoiYXBpLm5zZSIsImlhdCI6MTYwMzY3ODAxNiwiZXhwIjoxNjAzNjgxNjE2fQ.W5Xzssxssvmw3f5pO6bX_ODxws08no2TeLpqkAlIdZ8
