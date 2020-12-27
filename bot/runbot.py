from time import sleep

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
import sys

sys.path.insert(1, '../bot/')
def RunBot(personal_data, target_product):  # function which will run after press the button 'Start purchase'

    main_url = 'https://www.supremenewyork.com/shop/all/'

    options = webdriver.ChromeOptions()
    options.add_extension('anticaptcha-plugin_v0.50.crx')
    options.add_argument('lang=en')
    driver = webdriver.Chrome('../bot/chromedriver.exe', options=options)

    driver.get(main_url + target_product['type'])  # loads the url where the product is placed

    # the bot is developed to perform during the drops, so, it will wait refreshing the page until the product appears
    '''bot.wait_product(target_product['name'])'''
    while (True):

        wrap = WebDriverWait(driver, 10).until( #  after refresh searchs the main wrap
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[id="wrap"]')))

        try:  # then checks if the product has appeared, if not an exception is raised
            wrap.find_element_by_partial_link_text(target_product['name']).click()

        except NoSuchElementException:  # if raises then refresh every second
            driver.refresh()
            sleep(1)
            continue
        break

    WebDriverWait(driver, 3).until( # selects de color
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'a[data-style-name="{}"]'.format(target_product['color'])))
                ).click()

    if target_product['size'] != 'no size available': # if available, selects the size
        Select(
            WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'select[name="size"]'))
                    )).select_by_visible_text(target_product['size'])
        sleep(0.1)  # time to send size info

    '''bot.submit()'''
    driver.switch_to.default_content()  # when we add something to cart a new frame appears, we switch to default

    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'input[type=submit]'))
                ).click()

    '''bot.check_out()'''
    WebDriverWait(driver, 5).until( # go to checkout frame
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'a[class="button checkout"]'))
                ).click()

    wrap = WebDriverWait(driver, 10).until( # checks if the new wrap is visible
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'div[id="wrap"]')))

    wrap.find_element_by_css_selector('input[placeholder="full name"]').send_keys(personal_data['name'])
    wrap.find_element_by_css_selector('input[placeholder="email"]').send_keys(personal_data['email'])
    wrap.find_element_by_css_selector('input[placeholder="tel"]').send_keys(personal_data['telephone'])
    wrap.find_element_by_css_selector('input[placeholder="address"]').send_keys(personal_data['address'])
    wrap.find_element_by_css_selector('input[placeholder="city"]').send_keys(personal_data['city'])
    wrap.find_element_by_css_selector('input[placeholder="postcode"]').send_keys(personal_data['postcode'])

    Select(
        wrap.find_element_by_css_selector('select[name="order[billing_country]"]')
            ).select_by_value(personal_data['country'])

    # we always pay with paypal, it is faster than VISA because it requires double step purchase confirmation by sms
    # paypal just requires login and confirmation in their page
    wrap.find_element_by_xpath("//select[@id='credit_card_type']/option[text()='PayPal']").click()
    wrap.find_elements_by_css_selector('div[class="icheckbox_minimal"]')[1].click()
    wrap.find_element_by_css_selector('input[name="commit"]').click()

    # At this point probably recaptcha v.3 has sent us some challenge. The program will wait until
    # anti-recaptcha.com chrome extension do his work bypassing the antibots, it can take a few seconds or a whole minute.
    # It could be a good idea to implement a VPN service at this part of the program to avoid the challenges

    # During the drops the page can crash and a message appears. If it appears the bot restarts the purchase

    if len(driver.find_elements_by_css_selector('div[class="failed"]')) != 0:
        RunBot(personal_data, target_product)

    driver.switch_to.default_content()

    email_box = WebDriverWait(driver, 300).until(  # paypal page can be very slow to load...
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, 'input[id="email"]')))
    email_box.send_keys(personal_data['paypal email'])
    email_box.send_keys(Keys.RETURN)

    '''WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'input[id="email"]'))
                ).send_keys(Keys.RETURN)'''

    # sleep(2)  # time to load the password box

    driver.switch_to.default_content()

    password_box = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable(
                            (By.CSS_SELECTOR, 'input[id="password"]')))
    password_box.send_keys(personal_data['paypal password'])
    password_box.send_keys(Keys.RETURN)

    '''WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button[id="payment-submit-btn"]'))
                ).click()'''

    return

def ScrapLatestDroplist():  # drop list scraper

    # searching which is the latest drop
    response = requests.get('https://www.supremecommunity.com/droplists/')
    soup = BeautifulSoup(response.content, 'html.parser')

    # getting the url where are the products info
    latest_drops = soup.find('div', id='box-latest').find('a')['href']
    main_url = 'https://www.supremecommunity.com'+latest_drops
    # lets scrap the info to put it in the GUI selectors

    options = webdriver.ChromeOptions()
    options.add_argument('lang=en')
    driver = webdriver.Chrome('../bot/chromedriver.exe', options=options)

    driver.get(main_url)
    drop_products = driver.find_elements_by_css_selector('div[class="card card-2"]')

    result = []

    for product in drop_products:

        product.find_element_by_css_selector('h2[class="name item-details item-details-title"]').click()
        sleep(2)

        product_info_tab = driver.find_element_by_css_selector('div[class="modal-content"]')

        # ----------------------getting likes, dislikes, name and release info------------------------
        likes = product_info_tab.find_element_by_css_selector('p[class="upvotes hidden"]').get_attribute('innerHTML')
        dislikes= product_info_tab.find_element_by_css_selector('p[class="downvotes hidden"]').get_attribute('innerHTML')
        name = product_info_tab.find_element_by_css_selector('h1[class="detail-title"]').get_attribute('innerHTML')

        release = product_info_tab.find_element_by_css_selector('h2[class="details-release-small"]')
        release = release.find_element_by_tag_name('span').get_attribute('innerHTML')

        # ----------------------getting colors and prices info------------------------

        product_descriptions = product_info_tab.find_element_by_css_selector('ul[class="tabs-content"]')
        details = product_descriptions.find_elements_by_css_selector('li')

        details_result = [] # [0] = prices, [1] = colors
        for detail in details[1:3]:
            detail_info = detail.find_elements_by_css_selector('span')
            details_result.append([x.get_attribute('innerHTML') for x in detail_info])

        # -----------------getting sizes info------------------------------------------------------------


        table_head = product_descriptions.find_elements_by_css_selector('th')[1:]
        sizes = [size.get_attribute('innerHTML') for size in table_head]

        if len(sizes) == 0:
            sizes = ['no sizes available']

        product_info_tab.find_element_by_css_selector('button[data-dismiss="modal"]').click()

        # Now he have to convert the sizes to Supreme shop size labels
        transformation = {'M': 'Medium', 'L': 'Large', 'XL': 'XLarge', 'S': 'Small'}
        sizes_transformed = [transformation[size] if size in ['S', 'M', 'L', 'XL'] else 'no size available' for size in sizes]

        # sometimes color strings have a whitespace at the beginning, we will rmeove that ws
        for k in range(len(details_result[1])):
            if details_result[1][k][0] == ' ':
                details_result[1][k] = details_result[1][k][1:]

        product_dict = {'release': release, 'name': name, 'color': details_result[1], 'sizes':sizes_transformed,
                    'prices': details_result[0], 'likes': likes, 'dislikes': dislikes}

        print(product_dict)
        result.append(product_dict)

    pd.DataFrame(result).to_csv('supreme-droplist.csv', sep=';', index=False)
    driver.close()
    return