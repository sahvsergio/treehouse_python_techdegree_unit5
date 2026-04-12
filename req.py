import requests
import json
import os
import traceback

TREEHOUSE_DATA= os.getenv('TREEHOUSE_DATA')
print(f"DEBUG:The URL is {TREEHOUSE_DATA}")

try:
    my_info = requests.get(TREEHOUSE_DATA)
    data=my_info.json()
except Exception:
    print("""---ERROR DETECTED---""")
    traceback,print_exc()
    
with open('treehouse.json','w') as treehouse_info:
    json.dump(data, treehouse_info, indent=4)
    


   
    

