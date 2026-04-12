import requests
import json
import os
import traceback

TREEHOUSE_DATA= os.getenv('TREEHOUSE_DATA')
print(f"DEBUG:The URL is {TREEHOUSE_DATA}")
try:
    my_info = requests.get(TREEHOUSE_DATA)
except Exception:
    print("""---ERROR DETECTED---""")
    traceback,print_exc()
    
with open('treehouse.json','w') as treehouse_info:
    treehouse_info.write(str(my_info.text))
    


   
    

