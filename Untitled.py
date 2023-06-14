import os
import random
import string
import time
import warnings

import requests
from lxml.html import fromstring
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

warnings.filterwarnings("ignore", category=DeprecationWarning) 

if not os.path.exists("tokens.txt"):
    with open("tokens.txt", "w") as f:
        f.write('')
if not os.path.exists("users.txt"):
    with open("users.txt", "w") as f:
        f.write('')

file = open("users.txt", 'a')

def get_proxies():
    url = 'https://sslproxies.org/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = []
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.append(proxy)
    return proxies

def start(proxy):
    token = None

    def get_random_login(length: int = 8):
        global file
        # Getting a random email
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        driver.find_element(By.XPATH, "//input[@name='email']").send_keys(result_str + '@wp2.pl')
        file.write("\n email: " + result_str +"@wp2.pl\n")

        # Getting a random username
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        driver.find_element(By.XPATH, "//input[@name='username']").send_keys(result_str)
        file.write("username: " + result_str + "\n")

        # Getting a random password
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        driver.find_element(By.XPATH, "//input[@name='password']").send_keys("!" + result_str)
        file.write("password: " + "!" + result_str)
    
    def finish():
        driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div[1]/div/div/div/form/div/div/div[4]/div[1]/div[1]/div/div/div/div/div[1]/div[1]").click()
        driver.find_element(By.ID, "react-select-2-option-0").click()
        driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div[1]/div/div/div/form/div/div/div[4]/div[1]/div[2]/div/div/div/div/div[1]/div[1]").click()
        driver.find_element(By.ID, "react-select-3-option-0").click()
        driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div[1]/div/div/div/form/div/div/div[4]/div[1]/div[3]/div/div/div/div/div[1]").click()
        driver.find_element(By.ID, "react-select-4-option-17").click()

        driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div[1]/div/div/div/form/div/div/div[5]/label/input").click()
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

    option = webdriver.ChromeOptions()
    option.add_argument("--mute-audio")
    option.add_argument(f'--proxy-server=http://{proxy}')
    option.add_argument("--headless")
    option.add_extension("dknlfmjaanfblgfdfebhijalfmhmjjjo.zip")
    option.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(options = option)
    driver.get('https://discord.com/register')

    time.sleep(2)
    print('Generating Token...')
    get_random_login()
    finish()

    while token is None:
        token = driver.execute_script("""return (webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m).find(m=>m?.exports?.default?.getToken!==void 0).exports.default.getToken()""")
        if token is None:pass
        else:
            print(f'Token Generated! {token}')
            with open('tokens.txt', 'a') as f:
                f.write(f"\n{token}")
            driver.quit()

amount = int(input('How Many Tokens Would you like to generate: '))
proxies = get_proxies()
proxy_pool = iter(proxies)

for run in range(amount):
    proxy = next(proxy_pool)
    print(f"using proxy {proxy}")
    start(proxy)

file.close()
