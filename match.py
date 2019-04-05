import pandas as pd
import tkinter as tk
from tkinter import messagebox


class Application(tk.Frame):
    def __init__(self, master=None, bugs=None, devices=None, testers=None, tester_device=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.bugs = bugs
        self.devices = devices
        self.testers = testers
        self.tester_device = tester_device

        self.device_options = ['*ALL*']
        self.country_options = ['*ALL*']

        self.specified_devices = []
        self.specified_countries = []

        self.tester_count = {}
        self.device_map = {}
        self.tester_map = {}

        self.res = []

        self.create_options()
        self.create_widgets()

    def create_options(self):
        for row in self.devices.itertuples(): 
            self.map_devices(row = row)
            self.device_options.append(row.description)

        for row in self.testers.itertuples():
            if row.country not in self.country_options: 
                self.country_options.append(row.country)

    def map_devices(self, row):
        # Name -> ID for devices 
        if row.description not in self.device_map:
            self.device_map[row.description] = row.deviceId

    def map_testers(self):
        # ID -> Name for testers based on current country restrictions
        for row in self.testers.itertuples(): 
            if row.country in self.specified_countries: 
                if row.testerId not in self.tester_map: 
                    self.tester_map[row.testerId] = row.firstName + ' ' + row.lastName

    def add_device(self): 
        if len(self.device_list.curselection()) != 0:
            curr_selection = self.device_options[self.device_list.curselection()[0]]
            if curr_selection not in self.specified_devices: 
                self.specified_devices.append(curr_selection)
                self.device_selection.insert(0, curr_selection)

    def add_country(self): 
        if len(self.country_list.curselection()) != 0: 
            curr_selection = self.country_options[self.country_list.curselection()[0]]
            if curr_selection not in self.specified_countries: 
                self.specified_countries.append(curr_selection)
                self.country_selection.insert(0, curr_selection)
    
    def remove_device(self): 
        curr_selection = self.device_options[self.device_selection.curselection()[0]]
        self.device_selection.delete(0)
        self.specified_devices.remove()

    def remove_country(self): 
        pass
    
    def create_widgets(self):
        self.country_block()
        self.device_block()
        self.command_block()

    def country_block(self):
        self.country_label = tk.Label(self, text="Possible Countries:")
        self.country_selection_label = tk.Label(self, text="Countries to Search On:")
        self.country_list = tk.Listbox(self)

        for i, option in enumerate(self.country_options):
            self.country_list.insert(i, option) 

        self.country_selection = tk.Listbox(self)
        self.add_country = tk.Button(self, text = "ADD", fg = "blue", command = self.add_country)
        self.remove_country = tk.Button(self, text = "REMOVE", fg = "red", command = self.remove_country)

        self.country_label.grid(row = 0, column = 0, padx = 10)
        self.country_list.grid(row = 1, column = 0, padx = 10, pady=30)
        self.add_country.grid(row = 1, column = 1)
        self.country_selection_label.grid(row = 0, column = 3)
        self.country_selection.grid(row = 1, column = 3, padx = 10)
        self.remove_country.grid(row = 1, column = 5, padx = 10)

    def device_block(self):
        self.device_label = tk.Label(self, text="Possible Devices:")
        self.device_selection_label = tk.Label(self, text="Devices to Search On:")
        self.device_list = tk.Listbox(self)

        for i, option in enumerate(self.device_options):
            self.device_list.insert(i, option) 

        self.device_selection = tk.Listbox(self)
        self.add_device = tk.Button(self, text = "ADD", fg = "blue", command = self.add_device)
        self.remove_device = tk.Button(self, text = "REMOVE", fg = "red", command = self.remove_device)

        self.device_label.grid(row = 2, column = 0)
        self.device_list.grid(row = 3, column = 0)
        self.add_device.grid(row = 3, column = 1)
        self.device_selection_label.grid(row = 2, column = 3)
        self.device_selection.grid(row = 3, column = 3)
        self.remove_device.grid(row = 3, column = 5)

    def command_block(self):
        self.submit = tk.Button(self, text = "RUN", fg="green", command=self.run)
        self.submit.grid(row = 4, column = 0, columnspan = 2, padx = 20)


    def translate_device(self, device):
        return self.device_map[device]

    def find_match(self): 
        # Populate tester_count based on specified devices 
        for row in self.bugs.itertuples(): 
            for device in self.specified_devices: 
                if row.deviceId == device: 
                    if row.testerId not in self.tester_count: 
                        self.tester_count[row.testerId] = 1
                    else:
                        self.tester_count[row.testerId] += 1


    def translate_testers(self):
        # Retranslate testerId using tester_map that has only included relevant testers and output to a list
        self.map_testers()
        sorted_tester_count = sorted(self.tester_count.items(), key=lambda x: x[1])[::-1]
        for k, v in sorted_tester_count:
            if k in self.tester_map: 
                self.res.append('Tester: ' + self.tester_map[k]+ ', ' + 'Bugs: ' + str(v))

    def output(self): 
        if len(self.res) == 0: 
            messagebox.showinfo("Results:", "No Results")
        else:
            output_string = ""
            for i, result in enumerate(self.res, 1): 
                output_string += (str(i) + '. ' + result + "\n\n")
            messagebox.showinfo("Results:", output_string)
            print(output_string)
        
    def run(self):
        self.specified_devices = [self.translate_device(device) for device in self.specified_devices]
        self.find_match()
        self.translate_testers()
        self.output()

bugs = pd.read_csv('bugs.csv')
devices = pd.read_csv('devices.csv')
testers = pd.read_csv('testers.csv')
tester_device = pd.read_csv('tester_device.csv')

root = tk.Tk()
app = Application(root, bugs, devices, testers, tester_device)
app.mainloop()






