from time import sleep,time
from main import SupremeBot
import json

special_chars = ['®']

def RunBot(personaldata_dict, target_product, init_hour):

bot = SupremeBot()

bot.init_products_page('shirts')

bot.wait_product('Chains')
# t0 = time()
bot.get_product('Chains', 'White','Medium')

bot.submit()

sleep(0.2)

bot.check_out()

sleep(0.2)

# t1 = time()
# print('product buyed in: ', t1-t0, 'sec')

bot.fill_personal_data_and_commit(personaldata_dict)

# t2 = time()
# print('data filled in: ', t2-t1, 'sec,', 'amount: ', t2-t0)

bot.fill_paypal_data(personaldata_dict)

# t3 = time()
# print('paypal payment done in: ', t3-t2, 'sec', 'amount:', t3-t0)