import requests

BASE = "http://127.0.0.1:5000/"
     
# response = requests.get(BASE + "feed/98765")
# print(response.json())
response = requests.get(BASE + "feed/12345")
print(response.json())
#input()
#response = requests.put(BASE + "feed/12345", {"feedid":100, "url":"https://thebright.com/feed/", "trackinggroup":12345})
#print(response.json())
#input()
#response = requests.patch(BASE + "feed/12345")
#print(response.json())

