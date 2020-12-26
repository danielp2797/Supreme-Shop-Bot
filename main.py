from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import pandas as pd
from selenium.webdriver.support.ui import Select
import requests

driver_PATH = 'C:/Program Files (x86)/chromedriver.exe'
main_url = 'https://www.supremenewyork.com/shop/all/'

options = webdriver.ChromeOptions()
options.add_argument('lang=en'), options.add_extension('reCAPTCHA/Buster Captcha Solver for Humans.crx')
options.add_extension('reCAPTCHA/anticaptcha-plugin_v0.50.zip')
driver = webdriver.Chrome(driver_PATH, options=options)

def category(name = ''):
    return main_url + name

def saveFile(content,filename):
    with open(filename, "wb") as handle:
        for data in content.iter_content():
            handle.write(data)

def search_product_link(data, names_colors_array): # pd.DataFrame, list of tuples (name, color)

    links = []

    for item in names_colors_array:
        links.append((data[(data['name'] == item[0]) & (data['color'] == item[1])]['link'].iloc[0]))

    return links

class SupremeBot:

    def get_all_products(self, type=''):

        driver.get(category(type))

        wrap = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[id="wrap"]')))

        articles = wrap.find_elements_by_tag_name('article')
        links = [article.find_element_by_tag_name('a').get_attribute('href') for article in articles]
        names = [article.find_element_by_tag_name('h1').find_element_by_tag_name('a').text for article in articles]
        color = [article.find_element_by_tag_name('p').find_element_by_tag_name('a').text for article in articles]

        result = np.array(list(zip(names, color, links)))
        result = result.reshape(len(names), 3)

        return pd.DataFrame(result, columns=['name', 'color', 'link'])

    def products_to_cart(self, links):

        for link in links:

            driver.get(link)  # raises if product is sold out
            try:
                submit_button = WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type=submit]')))

            except:
                print('item is sold out: ', link)
                continue

            submit_button.click()
            sleep(0.5)
        sleep(0.5)

    def check_out(self):

        checkout_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[class="button checkout"]')))

        checkout_button.click()

    def fill_personal_data_and_commit(self, personaldata):  # dict

        wrap = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[id="wrap"]')))

        wrap.find_element_by_css_selector('input[placeholder="full name"]').send_keys(personaldata['name'])
        wrap.find_element_by_css_selector('input[placeholder="email"]').send_keys(personaldata['email'])
        wrap.find_element_by_css_selector('input[placeholder="tel"]').send_keys(personaldata['tel'])
        wrap.find_element_by_css_selector('input[placeholder="address"]').send_keys(personaldata['address'])
        wrap.find_element_by_css_selector('input[placeholder="city"]').send_keys(personaldata['city'])
        wrap.find_element_by_css_selector('input[placeholder="postcode"]').send_keys(personaldata['postcode'])
        
        # wrap.find_element_by_css_selector('input[placeholder="number"]').send_keys(personaldata['visa_number'])
        # wrap.find_element_by_css_selector('input[placeholder="CVV"]').send_keys(personaldata['visa_passcode'])
        
        # month_select = Select(wrap.find_element_by_css_selector('select[name="credit_card[month]"]'))
        # month_select.select_by_value(personaldata['visa_month'])

        # year_select = Select(wrap.find_element_by_css_selector('select[name="credit_card[year]"]'))
        # year_select.select_by_value(personaldata['visa_year'])

        country = Select(wrap.find_element_by_css_selector('select[name="order[billing_country]"]'))
        country.select_by_value(personaldata['order_country'])

        wrap.find_element_by_xpath("//select[@id='credit_card_type']/option[text()='PayPal']").click()
        
        wrap.find_elements_by_css_selector('div[class="icheckbox_minimal"]')[1].click()
        
        wrap.find_element_by_css_selector('input[name="commit"]').click()

    def get_product(self, name, color=None, size=None):

            wrap = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[id="wrap"]')))

            wrap.find_element_by_partial_link_text(name).click()

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-style-name="{}"]'.format(color)))).click()

            if size != None:

                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'select[name="size"]')))

                sleep(0.1)
                size_selector = Select(driver.find_element_by_css_selector('select[name="size"]'))
                size_selector.select_by_visible_text(size)
                sleep(0.1)  # time to send size info

    def init_products_page(self, product_type):

        driver.get(category(product_type))

    def submit(self):
        
        driver.switch_to.default_content()

        submit_button = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type=submit]')))

        submit_button.click()
        
    def wait_product(self, name):
        
        while(True):
            
            wrap = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[id="wrap"]')))
            
            try:
                wrap.find_element_by_partial_link_text(name)
            except:
                driver.refresh()
                sleep(1.5)
                continue
            break
    
    def solve_recaptcha_buster(self):
    
        n = 0
    
        while (True):
    
            try:
                WebDriverWait(driver, 1).until(
                    EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[title='recaptcha challenge']")))
    
            except:
                print('reCAPTCHA solved successfully')
                driver.switch_to.default_content()
                return
    
            print('step: ', n)
            n = n + 1
        
            if (n % 5 == 0):
            
                try:
                    WebDriverWait(driver, 1).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, 'button[id="recaptcha-reload-button"]'))).click()
                    print('challenge refreshed!!')
                    sleep(0.5)
                except:
                    break
        
            try:
                WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[id="solver-button"]'))).click()
                sleep(2)  # solving time
            except:
                print('solver-button not found')
                break
    
            driver.switch_to.default_content()
            
    def fill_paypal_data(self, paypaldata):
        
        driver.switch_to.default_content()
        
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[id="email"]'))).send_keys(paypaldata['paypal_email'])

        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[id="email"]'))).send_keys(Keys.RETURN)

        sleep(1)

        driver.switch_to.default_content()
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[id="password"]'))).send_keys(paypaldata['paypal_password'])

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[id="password"]'))).send_keys(Keys.RETURN)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[id="payment-submit-btn"]'))).click()

    def solve_recaptcha_IBM(self):  # solves recaptcha audio challenges using IBM watson sources
        
        n=0
        WebDriverWait(driver, 1).until(
            EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[title='recaptcha challenge']")))

        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[id="recaptcha-audio-button"]'))).click()
        
        while(True):
    
            n = n + 1
            if n>6:
                return True
                break
            
            try:
                # refresh by default
                WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'button[id="recaptcha-reload-button"]'))).click()
                
                audio = WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'audio[id="audio-source"]'))).get_attribute('src')
            except:
                print('reCAPTCHA challenge successfully solved')
                driver.switch_to.default_content()
                return False
                
            audio_response = requests.get(audio, stream=True)
            saveFile(audio_response, 'audio_challenge.mp3')
            
            # put into IBM service and get response

            IBM_source = 'https://speech-to-text-demo.ng.bluemix.net/'

            driver.execute_script('''window.open("","_blank");''')
            driver.switch_to.window(driver.window_handles[1])

            driver.get(IBM_source)

            # Upload audio file
            sleep(1)
            root = driver.find_element_by_id('root').find_elements_by_class_name('dropzone _container _container_large')
            btn = driver.find_element(By.XPATH, '//*[@id="root"]/div/input')
            btn.send_keys('C:/Users/PcCom/Desktop/Programacion_Daniel/Python/bot_supreme/audio_challenge.mp3')

            # Converting audio to text
            sleep(8)

            text = driver.find_element_by_css_selector('div[data-id="Text"]').find_element_by_tag_name('span').text

            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            
            WebDriverWait(driver, 1).until(
                EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[title='recaptcha challenge']")))
            
            try:
                driver.find_element_by_css_selector('input[id="audio-response"]').send_keys(text)
                sleep(1)
                driver.find_element_by_css_selector('button[id="recaptcha-verify-button"]').click()
                sleep(1)
            except:
                print('reCAPTCHA challenge failed')
        
        
    
        













