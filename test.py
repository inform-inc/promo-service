import requests

BASE = "http://0.0.0.0:5000/"
     
# response = requests.get(BASE + "feed/98765")
# print(response.json())
#response = requests.get(BASE + "feed/93425")
#print(response.json())
#input()
response = requests.put(BASE + "feed/77008", {"feedid":103, "url":"https://thebright.com/feed/", "trackinggroup":93425})
print(response.json())

response = requests.get(BASE + "feed/77008")
print(response.json())
#response = requests.patch(BASE + "feed/12345")
#wprint(response.json())

