import requests
import json
from datetime import date, timedelta
#walidacja daty
class KimaiLoader:
    
    def __init__(self):
      print("hello")
    
    def authentication(self):
      name = "bartek"#input("login")
      password = "wafel123"#input("Twoje haslo")
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
      working_hours_start = "07:00:00"#input ("Podaj o ktorej zaczynasz prace eg 07:00:00")
      working_hours_end = "15:00:00"#input ("Podaj o ktorej konczysz prace eg 15:00:00")
      start = "2019-02-02"#input(" Podaj date od ktorej zaczynasz zmiane eg 2019-02-02")
      end = "2019-02-05"#input(" Podaj date koncowa eg 2019-02-05")
      day_list = self.between_dates(start,end,working_hours_start,working_hours_end)
      data_to_api=[]
      a = 0
      while a != len(day_list):
        data = {"projectId":1,"taskId":2,"start":day_list[a][0],"end":day_list[a][1],"commentType":"","statusId":1}
        data_to_api.append([data])
        a += 1
      b = 0
      while b != len(data_to_api):
        params = [api_key,data_to_api[b][0]]
        print(self.api_payload('setTimesheetRecord',params))
        b += 1
    def between_dates(self,start,end,start_h, end_h):
      d1 = date(int(start[:4]),int(start[5:7]),int(start[8:10]))
      d2 = date(int(end[:4]),int(end[5:7]),int(end[8:10])) 
      delta = d2 - d1
      days_range = []
      for i in range(delta.days + 1):
          append = d1 + timedelta(i)
          append_start = str(append) + " " + start_h
          append_end = str(append) + " " + end_h
          days_range.append([append_start,append_end])
      return days_range    
      
new= KimaiLoader()
auth = new.authentication()
api_key=new.catch_api_key(auth)
print(new.set_new_record(api_key))
# start = "2019-02-03"
# end = "2019-02-10"
# print(int(start[:4]))
# print(start[5:7])
# print(start[8:10])
 
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

