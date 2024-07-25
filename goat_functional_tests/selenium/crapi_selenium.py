import json
import re
import time
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from faker import Faker

def get_webdriver(browser):
    if browser == "CHROME":
        chrome_options = webdriver.ChromeOptions()
        pynt = os.environ.get("RUNNING_FROM_PYNT", "")
        if pynt == "True":
            # This section is only when running with Pynt
            chrome_options.add_argument('--proxy-server=http://127.0.0.1:6666')
            chrome_options.add_argument('--proxy-bypass-list=<-loopback>')
            chrome_options.add_argument("--ignore-certificate-errors")
    
        return webdriver.Chrome(options=chrome_options) 

def register_user():
    url = "http://localhost:8888/identity/api/auth/signup"
    fake = Faker()
    name = f"{fake.first_name()}.{fake.last_name()}"
    email = f"{name}@example.com"
    number = fake.msisdn()[:10]
    password = fake.password(length=16)

    payload = json.dumps({
        "name": name,
        "email": email,
        "number": number,
        "password": password
    })
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
        'Content-Type': 'application/json',
        'Accept': '*/*'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text, email)
    return email, password

def login_user(email, password):
    url = "http://localhost:8888/identity/api/auth/login"

    payload = json.dumps({
        "email": email,
        "password": password
    })
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
        'Content-Type': 'application/json',
        'Accept': '*/*'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    
    return response.json().get("token", "")

def register_vehicle(email):
    url = f"http://localhost:8025/api/v2/search?kind=to&query={email}&limit=10"
    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
        mails = json_data.get("items", [])

        if len(mails) > 0:
            mail = mails[0]
            mbody = re.sub(r"[^a-zA-Z0-9<>:]*\n", "", mail['Raw']['Data'])

            vintext = re.search(r'VIN(.*)Pincode', mbody, re.I)
            if vintext:
                vin_match = re.search(r'>([A-Za-z0-9]+)<', vintext.group(1))
                if vin_match:
                    VIN = vin_match.group(1)                

            pintext = re.search(r'Pincode(.*)We\'re', mbody)
            if pintext:
                pin_match = re.search(r'>([0-9]+)<', pintext.group(1))
                if pin_match:
                    PIN = pin_match.group(1)                    
            vehicle = {"VIN": VIN, "PIN": PIN}
            print(vehicle)   
            return vehicle
    else:
        print(f"Request failed with status code: {response.status_code}")
        return None

def add_vehicle(vehicle, token):
    url = "http://localhost:8888/identity/api/v2/vehicle/add_vehicle"
    payload = json.dumps({
        "vin": vehicle["VIN"],
        "pincode": vehicle["PIN"],
    })
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Authorization': f'Bearer {token}'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

def get_vehicle(token):
    url = "http://localhost:8888/identity/api/v2/vehicle/vehicles"
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Authorization': f'Bearer {token}'
    }
    response = requests.request("GET", url, headers=headers)
    print(response.text)

def login_page(driver, creds):
    driver.get("http://localhost:8888/login")
    driver.implicitly_wait(10.5)
    text_box = driver.find_element(by=By.ID, value="basic_email")
    pass_box = driver.find_element(by=By.ID, value="basic_password")
    button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    text_box.send_keys(creds[0])
    pass_box.send_keys(creds[1])
    button.click()
    time.sleep(3)

def dashboard_page(driver):
    button_element = driver.find_element(By.XPATH, '//button[contains(@class, "ant-btn ant-btn-round ant-btn-primary ant-btn-lg") and .//span[@aria-label="sync"]]')
    actions = ActionChains(driver)
    actions.move_to_element(button_element).click().perform()
    
    refresh_button = driver.find_element(By.XPATH, "//button[.//span[text()='Refresh Location']]")
    refresh_button.click()
    time.sleep(3)

def logout(driver):
    div_element = driver.find_element(By.XPATH, '//div[contains(@class, "ant-dropdown-trigger nav-items") and .//span[@aria-label="down"]]')
    actions = ActionChains(driver)
    actions.move_to_element(div_element).perform()
    logout_button = driver.find_element(By.XPATH, '//span[contains(@class, "ant-dropdown-menu-title-content") and .//span[@aria-label="logout"] and contains(., "Logout")]')
    actions.move_to_element(logout_button).click().perform()

def teardown(driver):
    driver.quit()

def run_tests():
    # Two users are registered and logged in
    for _ in range(2):
        driver = get_webdriver("CHROME")
        creds = register_user()
        token = login_user(creds[0], creds[1])
        vehicle = register_vehicle(creds[0])
        add_vehicle(vehicle, token)
        get_vehicle(token)
        time.sleep(3)
        login_page(driver, creds)
        dashboard_page(driver)
        logout(driver)    
        teardown(driver)

if __name__ == "__main__":
    run_tests()
