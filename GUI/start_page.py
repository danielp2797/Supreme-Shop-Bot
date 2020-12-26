import tkinter as tk

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcome to the Supreme Shop Bot!", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Go to personal data",
                            command=lambda: controller.show_frame("DataPage"))
        button2 = tk.Button(self, text="Go to buy planner",
                            command=lambda: controller.show_frame("PurchasePage"))
        button1.pack()
        button2.pack()