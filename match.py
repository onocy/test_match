import pandas as pd

import tkinter as tk
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
            self.map_devices(row)
            self.device_options.append(row.description)

        for row in self.testers.itertuples():
            self.map_testers(row)
            if row.country not in self.country_options: 
                self.country_options.append(row.country)

    def map_devices(self, row):
        # Name -> ID for devices 
        if row.description not in self.device_map:
            self.device_map[row.description] = row.deviceId

    def map_testers(self, row):
        # ID -> Name for testers based on current country restrictions
        if row.country in self.specified_countries: 
            if row.testerId not in self.tester_map: 
                self.tester_map[row.testerId] = row.firstName + ' ' + row.lastName

    def add_device(self): 
        pass

    def add_country(self): 
        pass
    
    def remove_device(self): 
        pass

    def remove_country(self): 
        pass
    
    def create_widgets(self):
        self.country_label = tk.Label(self, text="Country:")
        self.country_list = tk.Listbox(self)

        for i, option in enumerate(self.country_options):
            self.country_list.insert(i, option) 

        self.country_selection = tk.Listbox(self)

        self.device_label = tk.Label(self, text="Device:")

        self.device_list = tk.Listbox(self)

        for i, option in enumerate(self.device_options):
            self.device_list.insert(i, option) 

        self.device_selection = tk.Listbox(self)

        self.submit = tk.Button(self, text = "RUN", fg="blue", command=self.run)

        self.add_device = tk.Button(self, text = "ADD", command = self.add_device)
        self.remove_device = tk.Button(self, text = "REMOVE", command = self.remove_device)

        self.add_country = tk.Button(self, text = "ADD", command = self.add_country)
        self.remove_country = tk.Button(self, text = "REMOVE", command = self.remove_country)

        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)

        self.country_label.grid(row = 0, column = 0)
        self.country_list.grid(row = 0, column = 1)
        self.add_country.grid(row = 0, column = 2)
        self.country_selection.grid(row = 0, column = 3)
        self.remove_country.grid(row = 0, column = 4)

        self.device_label.grid(row = 1, column = 0)
        self.device_list.grid(row = 1, column = 1)
        self.add_device.grid(row = 1, column = 2)
        self.device_selection.grid(row = 1, column = 3)
        self.remove_device.grid(row = 1, column = 4)

        self.submit.grid(row = 2, column = 0)
        self.quit.grid(row = 2, column = 1)


    def run(self):
        self.map_devices()
        self.map_testers()
        self.specified_devices = []
        self.specified_devices.append(self.device.get())
        self.specified_countries.append(self.country.get())
        self.specified_devices = [self.translate_device(device) for device in self.specified_devices]
        self.find_match()
        self.translate_testers()
        self.output()


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
        for k, v in self.tester_count.items(): 
            if k in self.tester_map: 
                self.res.append(self.tester_map[k] + ' => ' + str(self.tester_count[k]))

    def output(self): 
        tkMessageBox.showinfo(self.res)
        print(self.res)
        


bugs = pd.read_csv('bugs.csv')
devices = pd.read_csv('devices.csv')
testers = pd.read_csv('testers.csv')
tester_device = pd.read_csv('tester_device.csv')

root = tk.Tk()
app = Application(root, bugs, devices, testers, tester_device)
app.mainloop()






