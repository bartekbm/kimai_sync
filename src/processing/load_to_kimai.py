import requests
import json
#walidacja daty
class KimaiLoader:
    
    def __init__(self):
      print("hello")
    
    def authentication(self):
      name = input("Twoj login")
      password = input("Twoje haslo")
      params = [name,password]
      return self.api_payload('authenticate',params)
  
    def api_payload(self,method,params):
      payload={
        "method": method,
        "params": params,
        "id": "1",
        "jsonrpc": "2.0"
      }
      return self.json_dump(payload)
    
    def json_dump(self,payload):
      dump = json.dumps(payload)
      return self.request(dump)
      
    def request(self,dump):
      web = 'http://192.168.0.164/kimai/core/json.php'
      r = requests.post(web,data=dump)
      return r.content
    
    def catch_api_key(self,string):
      json_data = json.loads(string)
      api_key=json_data['result']['items'][0]['apiKey']
      return api_key
    
    def set_new_record(self,api_key):
      
      start = input(" Podaj date startowa eg 2019-02-03 07:00:00")
      end = input(" Podaj date koncowa eg 2019-02-03 09:00:00")
      data = {"projectId":1,"taskId":2,"start":start,"end":end,"commentType":"","statusId":1}
      params = [api_key,data]
      return self.api_payload('setTimesheetRecord',params)
      
      
new= KimaiLoader()
auth = new.authentication()
api_key=new.catch_api_key(auth)
print(new.set_new_record(api_key))

    
# payload={
#   "method": "authenticate",
#   "params": [
#     "bartek",
#     "wafel123"
#   ],
#   "id": "1",
#   "jsonrpc": "2.0"
# }
# payload={
#   "method": "setTimesheetRecord",
#   "params": ["d894d5865a0a073385cf75da5",{"projectId":1,"taskId":2,"start":"2019-03-31 07:00:00","end":"2019-03-31 09:00:00","commentType":"","statusId":1}],
#   "id": "1",
#   "jsonrpc": "2.0"
# }
# json_dump = json.dumps(payload)
# web = 'http://192.168.0.164/kimai/core/json.php'
# r = requests.post(web,data=json_dump)

# json_data = json.loads(r.text)
# print(json_data['result']['items'][0]['apiKey'])
# print(r.url)

