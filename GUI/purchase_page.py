import tkinter as tk
from tkinter import ttk
import os
import pandas as pd
from ast import literal_eval
import json
import sys
sys.path.insert(1, '../')
from runbot import RunBot

products_data = pd.read_csv('droplist_scrapping/supreme-droplist.csv', sep=';')

class PurchasePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Purchase planner", font=controller.title_font)
        label.grid(row=0, column=1, padx=10, pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.grid(row=100, column=0, padx=10, pady=10)

        # ----------------------- profile selector--------------------------------------
        # In this part we will
        # first we search every json in the folder profiles
        json_files = [pos_json for pos_json in os.listdir('profiles/') if pos_json.endswith('.json')]
        profiles = [json_file.split('_')[0] for json_file in json_files] + ['None']
        selector_variable = tk.StringVar('')
        selector_variable.set('No profile selected')

        # then we list it in a drop down menu widget
        profile_selector = ttk.Combobox(self, values=profiles, width=30)
        profile_selector.set('Select your profile...')
        profile_selector.grid(row=1, column=1, padx=10, pady=10)
        # ---------------------------target product definition----------------------------------

        product_names = products_data['name'].tolist()
        selector_prod = ttk.Combobox(self, value=product_names, width=30)
        selector_prod.set('Select a product...')
        selector_prod.grid(row=2, column=1, padx=10, pady=10)

        def callback_size(eventObject):
            abc = eventObject.widget.get()
            product = str(selector_prod.get())
            sizes = products_data[products_data['name'] == product]['sizes'].iloc[0]
            sizes = literal_eval(sizes)
            size_selector.config(values=sizes)

        def callback_color(eventObject):
            abc = eventObject.widget.get()
            product = str(selector_prod.get())
            colors = products_data[products_data['name'] == product]['color'].iloc[0]
            colors = literal_eval(colors)
            color_selector.config(values=colors)

        size_selector = ttk.Combobox(self, width=30)
        size_selector.set('Select the size...')
        size_selector.grid(row=3, column=1, columnspan=2, padx=10, pady=10, sticky='w')
        size_selector.bind('<Button-1>', callback_size)

        color_selector = ttk.Combobox(self, width=30)
        color_selector.set('Select the color...')
        color_selector.grid(row=4, column=1, columnspan=2, padx=10, pady=10, sticky='w')
        color_selector.bind('<Button-1>', callback_color)

        #----------------------- working hour selection-------------------------------------
        hour_selector = ttk.Combobox(self, value=['0'+str(i) if i <= 9 else str(i) for i in range(24)],
                                     width=30)
        hour_selector.set('Select the hour (HH format)')
        hour_selector.grid(row=6, column=1, padx=10, pady=10)

        minute_selector = ttk.Combobox(self, value=['0' + str(i) if i <= 9 else str(i) for i in range(60)],
                                     width=30)
        minute_selector.set('Select minutes (MM format)')
        minute_selector.grid(row=6, column=2, padx=10, pady=10)

        #---------------------- product type selector---------------------------------------
        # this selector is useful to start in the page where the product is placed ex. pants, hats...
        product_types = ['jackets', 'shirts', 'tops_sweaters',
                         'sweatshirts', 'pants', 't-shirts', 'hats', 'bags', 'accessories', 'skate']
        type_selector = ttk.Combobox(self, width=30, value = product_types)
        type_selector.set('Select the product type...')
        type_selector.grid(row=5, column=1, columnspan=2, padx=10, pady=10, sticky='w')

        #------------------------------working button-------------------------------

        def select_profile():
            try:
                with open('profiles/' + str(profile_selector.get()) + '_profile.json') as json_file:
                    json_dict = json.load(json_file)
                    json_file.close()
                    return json_dict
            except FileNotFoundError:
                print('profile not found')

        def StartPurchase():

            personal_data = select_profile()
            product_info = {'name': str(selector_prod.get()),
                            'size': str(size_selector.get()),
                            'color': str(color_selector.get()),
                            'type': str(type_selector.get())}
            print(personal_data, product_info)
            RunBot(personaldata_dict=personal_data, target_product=product_info)

        button = tk.Button(self, text="OK", command=select_profile)
        button.grid(row=70, column=2)
        button = tk.Button(self, text="Start Purchase",
                           command=StartPurchase)
        button.grid(row=100, column=1, padx=10, pady=10)