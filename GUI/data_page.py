import tkinter as tk
from tkinter import ttk
import json

class DataPage(tk.Frame):  # in this page we will introduce our neccessary data to buy the products

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Personal data", font=controller.title_font)
        label.grid(row=1, column=1)

        field_labels = ["name", "telephone", "address",
                  "email", "city", "postcode", "paypal email", "paypal password"]
        entries = []
        for num, i in enumerate(field_labels):
            l = tk.Label(self, text=i)
            l.grid(row=num+2, column=0, ipadx=10)  # remove sticky if not required
            e = tk.Entry(self)
            e.grid(row=num+2, column=1, padx=10, pady=10, sticky='ew')  # remove sticky if not required
            entries.append(e)  # keep the entries in a list so you can retrieve the values later

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        country_selector = ttk.Combobox(self, values=['ES', 'UK'], width=30)
        country_selector.set('Select your country...')
        country_selector.grid(row=10, column=1, padx=10, pady=10)
        tk.Label(self, text='country').grid(row=10, column=0, ipadx=10)



        # buttons definition
        # ---------------------------return to star page button-------------------------------------
        return_button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        return_button.grid(row=100, column=0)

        #-------------------------- save data button ---------------------------------------------

        def save_entries():  # saves the entries into a JSON file to be used during the purchases
            introduced_values = []

            for entry in entries:
                introduced_values.append(entry.get())

            introduced_values.append(country_selector.get())

            costumer_info = dict(zip(field_labels + ['country'], introduced_values))
            with open('profiles/'+introduced_values[0]+'_profile.json', 'w') as fp:
                json.dump(costumer_info, fp)
            fp.close()

        save_button = tk.Button(self, text = "Save", command = save_entries)
        save_button.grid(row=100, column=1, pady=10)