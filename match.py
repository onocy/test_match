import pandas as pd

bugs = pd.read_csv('bugs.csv')
devices = pd.read_csv('devices.csv')
testers = pd.read_csv('testers.csv')
tester_device = pd.read_csv('tester_device.csv')


tester_count = {}
res = []

# For each input name in input list, translate to device ID and add to specified_devices using new device_map  
specified_devices = [1, 2]

# For each input country in input list add to specified_countries  
specified_countries = ['US', 'GB']

# Initialize map for name -> ID lookup on devices
device_map = {}
for row in devices.itertuples():
    if row.description not in device_map:
        device_map[row.description] = row.deviceId

# Initialize map for ID -> name lookup on testers based on current Country restrictions
tester_map = {}
for row in testers.itertuples(): 
    if row.country in specified_countries: 
        if row.testerId not in tester_map: 
            tester_map[row.testerId] = row.firstName + ' ' + row.lastName

# Iterate over bugs and begin population of tester_count based on specified devices
for row in bugs.itertuples(): 
    for device in specified_devices: 
        if row.deviceId == device: 
            if row.testerId not in tester_count: 
                tester_count[row.testerId] = 1
            else:
                tester_count[row.testerId] += 1

# Retranslate testerId and output to a list
for k, v in tester_count.items(): 
    if k in tester_map: 
        res.append(tester_map[k] + ' => ' + str(tester_count[k]))

# ['Taybin Rutkin => 125', 'Miguel Bautista => 49']
print(res)
