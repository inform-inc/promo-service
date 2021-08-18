import requests

BASE = "http://127.0.0.1:5000/"

data = [{"partnerURL" : "http://test.com/1"},
        {"partnerURL" : "http://test.com/2"},
        {"partnerURL" : "http://test.com/3"}]
#data = [{"partnerURL" : "http://test.com/1"},
#        {"partnerURL" : "http://test.com/2"},
#        {"url" : "http://test.com/3"}]


for i in range(len(data)):
    response = requests.put(BASE + "feed/" +str(i), data[i])
    print(response.json())

input()
# response = requests.get(BASE + "feed/98765")
# print(response.json())
response = requests.get(BASE + "feed/0")
print(response.json())
