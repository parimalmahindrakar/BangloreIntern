from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

def get_nseappid_updated():
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36"
    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(executable_path="./web_drivers/chromedriver", chrome_options=chrome_options) 
    driver.get('http://www.nseindia.com/get-quotes/derivatives?symbol=SBIN')
    print("\n\n")
    print(driver.get_cookies())
    print("\n\n")
    nseappid = driver.get_cookies()[-2]['value']
    print("[Updated nseappid] : ", nseappid)
    with open("nseappid.txt", 'w') as file:
        file.write(nseappid)

    driver.quit()

get_nseappid_updated()
