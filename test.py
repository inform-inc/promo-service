import requests

BASE = "http://0.0.0.0:5000/"
     
# response = requests.get(BASE + "feed/98765")
# print(response.json())
#response = requests.get(BASE + "feed/93425")
#print(response.json())
#input()
response = requests.put(BASE + "feed/93425", {"feedid":105, "url":"https://thebright.com/feed/", "trackinggroup":93425})
print(response.json())
response = requests.put(BASE + "feed/98765", {"feedid":106, "url":"https://popularmilitary.com/feed/", "trackinggroup":98765})
print(response.json())
#testing
#more testing
response = requests.get(BASE + "feed/93425")
print(response.json())
response = requests.patch(BASE + "feed/98765")
print(response.json())

