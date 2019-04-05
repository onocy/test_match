import pandas as pd

import tkinter as tk
class Application(tk.Frame):
    def __init__(self, master=None):
        # TKinter intializations
        super().__init__(master)
        self.master = master
        self.pack()

        # For each input name in input list, translate to device ID and add to specified_devices using new device_map  
        self.specified_devices = [1, 2]

        # For each input country in input list add to specified_countries  
        self.specified_countries = ['US', 'GB']
        self.tester_count = {}
        self.device_map = {}
        self.tester_map = {}
        self.res = []
        self.read_files()
        self.run()
        self.create_widgets()

    def run(self):
        self.map_devices()
        self.map_testers()
        self.find_match()
        self.translate_testers()

    def create_widgets(self):
        self.lbl = tk.Label(self, text=self.res[0])
        self.lbl.pack(side = "top")
        self.txt = tk.Entry(self, width=10)
        self.txt.pack(side = "top")

        self.lbl2 = tk.Label(self, text=self.res[1])
        self.lbl2.pack(side = "top")
        self.txt = tk.Entry(self, width=10)
        self.txt.pack(side = "top")

        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(side="bottom")
        
    def read_files(self): 
        self.bugs = pd.read_csv('bugs.csv')
        self.devices = pd.read_csv('devices.csv')
        self.testers = pd.read_csv('testers.csv')
        self.tester_device = pd.read_csv('tester_device.csv')

    def map_devices(self):
        # Name -> ID for devices 
        for row in self.devices.itertuples():
            if row.description not in self.device_map:
                self.device_map[row.description] = row.deviceId

    def map_testers(self):
        # ID -> Name for testers based on current country restrictions
        for row in self.testers.itertuples(): 
            if row.country in self.specified_countries: 
                if row.testerId not in self.tester_map: 
                    self.tester_map[row.testerId] = row.firstName + ' ' + row.lastName

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
        print(self.res)

root = tk.Tk()
app = Application(master=root)
app.mainloop()





