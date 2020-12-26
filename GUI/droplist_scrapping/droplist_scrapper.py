from time import sleep

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

def ScrapLatestDroplist():

    # searching which is the latest drop
    response = requests.get('https://www.supremecommunity.com/droplists/')
    soup = BeautifulSoup(response.content, 'html.parser')

    # getting the url where are the products info
    latest_drops = soup.find('div', id='box-latest').find('a')['href']
    main_url = 'https://www.supremecommunity.com'+latest_drops
    # lets scrap the info to put it in the GUI selectors

    driver_PATH = 'C:/Program Files (x86)/chromedriver.exe'
    options = webdriver.ChromeOptions()
    options.add_argument('lang=en')
    driver = webdriver.Chrome(driver_PATH, options=options)

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


