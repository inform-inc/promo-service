import requests

BASE = "http://0.0.0.0:5000/"
print("running test.py")   
# response = requests.get(BASE + "feed/98765")
# print(response.json())
#response = requests.get(BASE + "feed/93425")
#print(response.json())
#input()
#response = requests.put(BASE + "feed/93556", {"feedid":107, "url":"https://thebright.com/feed/", "trackinggroup":93556})
#print(response.json())
#response = requests.put(BASE + "feed/77008", {"feedid":108, "url":"https://thebright.com/feed/", "trackinggroup":77008})
#print(response.json())
#response = requests.put(BASE + "feed/93425", {"feedid":106, "url":"https://popularmilitary.com/feed/", "trackinggroup":93425})
#print(response.json())
response = requests.put(BASE + "feed/90924", {"feedid":109, "url":"https://coastguardnews.com/feed/", "trackinggroup":90924})
print(response.json())

response = requests.get(BASE + "feed/93556")
print(response.json())
response = requests.get(BASE + "feed/77008")
print(response.json())
response = requests.get(BASE + "feed/93425")
print(response.json())
response = requests.get(BASE + "feed/90924")
print(response.json())
#response = requests.patch(BASE + "feed/93425",{"url":"https://popularmilitary.com/feed/"})
#print(response.json())
print("end of test.py") 


