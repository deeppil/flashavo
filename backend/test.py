import requests

url = 'http://127.0.0.1:5000/generate'
payload = {"topics" : "BIG FAT CHUNGUS"}

res = requests.post(url, json=payload)
print(res.json())
