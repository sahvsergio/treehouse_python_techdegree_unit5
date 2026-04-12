import requests
import json
import os 

TREEHOUSE_DATA= os.getenv('TREEHOUSE_DATA')

my_info = requests.get(TREEHOUSE_DATA)


with open('treehouse.json','w') as treehouse_info:
    treehouse_info.write(str(my_info.text))

pwith
   
    

