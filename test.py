import re
import requests
from database import cursor,db,insert_device
def validation(prefix):
    d = {'0':'zero','1':'one','2':'two','3':'three','4':'four','5':'five','6':'six','7':'seven','8':'eight','9':'nine'}
    prefix = prefix.lower()
    prefix = re.sub('[^A-Za-z0-9]+', '', prefix)
    for i in prefix:
        if i.isdigit():
            prefix = prefix.replace(i,d[i])
    return prefix

url = "https://fonoapi.freshpixl.com/v1/getdevice?token=7c916a36f00e1dc3d906e1f993456539b77afed54fe286f0&device=iphone&brand=apple"

res = requests.get(url).json()

for i in res:
    device_name = i['DeviceName']
    query = validation(device_name)
    insert_device(device_name,query)
