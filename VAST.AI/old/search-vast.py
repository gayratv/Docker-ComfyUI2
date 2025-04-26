import requests
import json

url = "https://console.vast.ai/api/v0/search/asks/"

payload = {"q": {"gpu_name": {"eq":"RTX_3090"}}}
headers = {
   'Accept': 'application/json',
   'Content-Type': 'application/json',
   'Authorization': 'Bearer f92b765a9d15cc6e3eb2445a11111dd4768cbf6d9cc245d9dc3b376f06fe859c'
}

response = requests.request("PUT", url, headers=headers, data=payload)


# print(response.text)
with open("../vast-search.json", "w", encoding="utf-8") as file:
   file.write(response.text)