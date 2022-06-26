import json
from re import A
import requests
import csv
import os
from os.path import exists
from private import inverter_path
from private import pi_path
import sys

# api call
inverter_url = inverter_path

# storing files
file_path = pi_path

# Initialising the values, if there is an error, these would be reported.
PAC = 'Nan'  #Eenrgy generated @ this moment
IAC = 'Nan'  #AC current @ this moment
IDC = 'Nan'  #DC current @ this moment
VAC = 'Nan'  #AC voltage @ this moment
VDC = 'Nan'  #DC voltage @ this moment

en_ty = 'Nan' #Energy generated today
en_yr = 'Nan' #Energy generated in current year
en_tt = 'Nan' #Energy generated in total

DST = []      #Device status variable

# Assiging units
PAC_unt = 'W'
IAC_unt = 'A'
IDC_unt = 'A'
VAC_unt = 'V'
VDC_unt = 'V'

en_td_unt = 'Wh'
en_yr_unt = 'Wh'
en_tt_unt = 'Wh'

current_data = requests.get(inverter_url)
print(current_data)

if current_data.status_code != 200:
    sys.exit(1)

current_data_json = json.loads(current_data.text)

timestamp = current_data_json.get('Head').get('Timestamp')

date = timestamp.split('T')[0]
time = timestamp.split('T')[1].split('+')[0]

# cumulation data and status
en_td = current_data_json.get('Body').get('Data').get('DAY_ENERGY').get('Value')   #Energy generated today
en_yr = current_data_json.get('Body').get('Data').get('YEAR_ENERGY').get('Value')  #Energy generated in current year
en_tt = current_data_json.get('Body').get('Data').get('TOTAL_ENERGY').get('Value') #Energy generated overall

# device status variable, all captured as one sequence in a list
DST = current_data_json.get('Body').get('Data').get('DeviceStatus')
DST = [DST[x] for x in DST]

# power related variables
PAC = current_data_json.get('Body').get('Data').get('PAC').get('Value') #Eenrgy generated @ this moment
IAC = current_data_json.get('Body').get('Data').get('IAC').get('Value')  #AC current @ this moment
IDC = current_data_json.get('Body').get('Data').get('IDC').get('Value')  #DC current @ this moment
VAC = current_data_json.get('Body').get('Data').get('UAC').get('Value')  #AC voltage @ this moment
VDC = current_data_json.get('Body').get('Data').get('UDC').get('Value')  #DC voltage @ this moment

otpt_lst = [date + ' ' + time, PAC, IAC, IDC, VAC, VDC, en_td, en_yr, en_tt, DST[0], DST[1], DST[2], DST[3], DST[4], DST[5]]
otpt_hdr = ['datetime', 'PAC' + '(' + PAC_unt + ')', 'IAC' + '(' + IAC_unt + ')', 'IDC' + '(' + IDC_unt + ')', \
           'VAC' + '(' + VAC_unt + ')' , 'VDC' + '(' + VDC_unt + ')', 'DAY_ENERGY' + '(' + en_td_unt + ')',\
           'YEAR_ENERGY' + '(' + en_yr_unt + ')', 'TOTAL_ENERGY' + '(' + en_tt_unt + ')', 'DeviceStatus']

# writing the data to a csv
csv_file = os.path.join(file_path, str(date)+'.csv')
mode = 'w' if exists(csv_file) == False else 'a' # selecting mode to append or write if the file exist

with open(csv_file, mode, newline='') as csvfile:
    slr_wrtr = csv.writer(csvfile, delimiter=',')
    slr_wrtr.writerow(otpt_lst)

print('success')
