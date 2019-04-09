import requests
import json
from datetime import date, timedelta
from src.config.configure import Configuration
from requests_kerberos import HTTPKerberosAuth as rk

class KimaiLoader:
    
    def __init__(self):
        """itam"""

    def authentication(self,name,password):

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

    requests_list=[]
    green_list=[]

    def returned_requests(self,text):
        self.parse_list(text)

    def read_requests_list(self):
        return self.requests_list

    def read_green_list(self):
        return self.green_list

    def parse_list(self,text):
        try:
            json_data = json.loads(text)
        except:
            return ""

        try:
            text="\nWpis: " + str(json_data['result']['items'])
            self.requests_list.append(text)
        except KeyError:
            text="\nUwaga błąd: " + str(json_data['result']['error'])
            self.requests_list.append(text)

        text=" Status wykonania: " + str(json_data['result']['success'])
        self.requests_list.append(text)
        #self.requests_list.append('\nERROR!')
        self.green_list.clear()
        if json_data['result']['success'] == True:
            self.green_list.clear()
            self.requests_list.append('\nSUKCES!')
            self.green_list.append("Jestem zielony")
    def clear_requests_list(self):

        self.requests_list.clear()

    def request(self,dump):
        webConf=Configuration()
        website=webConf.readFromConfig()['website']
        #r = requests.post(web, data=dump, auth=HTTPKerberosAuth(), verify=False)
        #web = 'https://kimai.creditagricole/core/json.php'
        try:
            r = requests.post(website, data=dump)
            #r = requests.post(website, data=dump, auth=rk(), verify=False)
        except:
            r=""
            return r
        self.returned_requests(r.content)

        return r.content

    def catch_api_key(self,string):
      json_data = json.loads(string)
      api_key=json_data['result']['items'][0]['apiKey']
      return api_key

    

    def get_project(self,api_key):
        return self.api_payload('getProjects', [api_key,'includeTasks'])


    def catch_result(self,to_catch,tasks=None):
        json_data = json.loads(to_catch)
        catching= json_data['result']['items']
        result = []
        tasks_list=[]
        a=0
        while a != len(catching):
            project_id = catching[a].get('projectID')
            project_name = catching[a].get('name')
            customer_name=catching[a].get('customerName')
            project_name=f"{project_name} ({customer_name})"
            tasks=catching[a].get('tasks')

            i=0
            while i != (len(tasks)):
                name=tasks[i].get('name')
                id=tasks[i].get('activityID')
                tasks_list.append({"name":name,"id":id})

                i +=1
            result.append({'project_id':project_id,'project_name':project_name,'tasks_list':tasks_list})

            tasks_list=[]
            a += 1


        return result

    def set_new_record(self,api_key,start,end,working_hours_start,working_hours_end):

      day_list = self.between_dates(start,end,working_hours_start,working_hours_end)
      data_to_api=[]
      a = 0
      while a != len(day_list):
        conf = Configuration()
        data = {"projectId":conf.readFromConfig()['procject_value'],"taskId":conf.readFromConfig()['task_value'],"start":day_list[a][0],"end":day_list[a][1],"commentType":"","statusId":1,"location":"","comment":"","description":"","trackingNumber":"","budget":"","billable":"","approved":"","cleared":""}

        data_to_api.append([data])
        a += 1
      b = 0
      while b != len(data_to_api):
        params = [api_key,data_to_api[b][0]]
        self.api_payload('setTimesheetRecord',params)
        b += 1
    def between_dates(self,start,end,start_h, end_h):
      if int(start_h[:2]) > int(end_h[:2]):
          d1 = date(int(start[:4]), int(start[5:7]), int(start[8:10]))
          d2 = date(int(end[:4]), int(end[5:7]), int(end[8:10]))
          delta = d2 - d1
          days_range = []
          for i in range(delta.days + 1):
              append = d1 + timedelta(i)
              append_night= append + timedelta(days=1)
              append_start = str(append) + " " + start_h
              append_end = str(append_night) + " " + end_h
              days_range.append([append_start, append_end])
          return days_range

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

