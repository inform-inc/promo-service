import requests

BASE = "http://localhost:5000/"
     
# response = requests.get(BASE + "feed/98765")
# print(response.json())
response = requests.get(BASE + "feed/93425")
print(response.json())
input()
response = requests.put(BASE + "feed/93425", {"feedid":102, "url":"https://popularmilitary.com/feed/", "trackinggroup":93425})
#print(response.json())
#input()
response = requests.get(BASE + "feed/93425")
print(response.json())
#response = requests.patch(BASE + "feed/12345")
#print(response.json())

