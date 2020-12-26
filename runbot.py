from time import sleep,time
from bot import SupremeBot

def RunBot(personaldata_dict, target_product):

    bot = SupremeBot()

    bot.init_products_page(target_product['type'])

    bot.wait_product(target_product['name'])
    # t0 = time()
    bot.get_product(target_product['name'], target_product['color'], target_product['size'])

    bot.submit()

    sleep(0.2)

    bot.check_out()

    sleep(0.2)

    # t1 = time()
    # print('product buyed in: ', t1-t0, 'sec')

    bot.fill_personal_data_and_commit(personaldata_dict)

        # t2 = time()
    # print('data filled in: ', t2-t1, 'sec,', 'amount: ', t2-t0)

    sleep(1)
    if bot.check_if_supreme_web_is_busy():
        RunBot(personaldata_dict, target_product)
    else:
        pass

    bot.fill_paypal_data(personaldata_dict)

    # t3 = time()
    # print('paypal payment done in: ', t3-t2, 'sec', 'amount:', t3-t0)