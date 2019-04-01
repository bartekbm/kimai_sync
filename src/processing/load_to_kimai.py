import requests
import json
from datetime import date, timedelta
from src.config.configure import Configuration


#walidacja daty
class KimaiLoader:
    
    def __init__(self):
      print("hello")
    
    def authentication(self,name,password):

      params = [name,password]
      return self.api_payload('authenticate',params)
  
    def api_payload(self,method,params):
      print(params)
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
        r = requests.post(web, data=dump)
        return r.content
    
    def catch_api_key(self,string):
      json_data = json.loads(string)
      api_key=json_data['result']['items'][0]['apiKey']
      return api_key
    
    # def get_customer(self,api_key):
    #     return self.api_payload('getCustomers',[api_key])

    def get_project(self,api_key):
        return self.api_payload('getProjects', [api_key,'includeTasks'])

    # def get_tasks(self,api_key):
    #     return self.api_payload('getTasks', [api_key])

    def catch_result(self,to_catch,tasks=None):
        json_data = json.loads(to_catch)
        catching= json_data['result']['items']
        #print(f"drukuje to co bedzie parsowane {catching}")
        #print(len(catching))
        result = []
        tasks_list=[]
        print(catching)
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
            #print(project_id, project_name, customer_name,tasks_list)
            #result.append([project_id, project_name + (f" ({customer_name}) ",tasks_list)])
            result.append({'project_id':project_id,'project_name':project_name,'tasks_list':tasks_list})

            tasks_list=[]
            #print(result)
            a += 1
            # project_name= [catching][1][0]['name']
            # print(project_name)
            # customer_name= [catching][1][0]['customerName']
            # print(customer_name)
            # tasks = [catching][1][0]['tasks']
            # print(tasks)
        # print(catching)
        # print(len(catching))
        #while a != len(catching):
            # if tasks =='yes':
            #     id = json_data['result']['items'][a]['activityID']
            #     #print(f"drukuje id taska {id}")
            # else:
            #     id = json_data['result']['items'][a]['customerID']
            #     #print(f"drukuje id taska {id}")
            # name = json_data['result']['items'][a]['name']
            # name_customer = json_data['result']['items'][a]['customerName']
            #name_id_tasks = json_data['result']['items'][a]['tasks'][a]['activityID']
            # print(len(name_id_tasks))
            # name_tasks = json_data['result']['items'][a]['tasks'][a]['name']
            # print(f"Jestem 1 projekem, name {name}, customer to:, {name_customer}, task id {name_id_tasks}, nazwa {name_tasks}")
            # result.append([id,name])
            # #f"drukuje wynik cały {result}"
            # print(catching)
            # print(len(catching))
            # print(a)
            # a += 1
            # print(len(name_id_tasks))
            # i =0
            # while i != len(name_id_tasks):
            #     print(name_id_tasks)
            #     i += i

        print(result)
        return result

    def set_new_record(self,api_key,start,end,working_hours_start,working_hours_end):

      day_list = self.between_dates(start,end,working_hours_start,working_hours_end)
      data_to_api=[]
      a = 0
      while a != len(day_list):
        conf = Configuration()
        data = {"projectId":conf.readFromConfig()['procject_value'],"taskId":conf.readFromConfig()['task_value'],"start":day_list[a][0],"end":day_list[a][1],"commentType":"","statusId":1,"location":"","comment":"","description":"","trackingNumber":"","budget":"","billable":"","approved":"","cleared":""}
        print(data)
        data_to_api.append([data])
        a += 1
      b = 0
      while b != len(data_to_api):
        params = [api_key,data_to_api[b][0]]
        print(self.api_payload('setTimesheetRecord',params))
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

#
# new= KimaiLoader()
# auth = new.authentication(name= 'bartek',password = 'wafel123')
# api_key=new.catch_api_key(auth)
# tasks=new.get_tasks(api_key)
# customer=new.get_customer(api_key)
# projects=new.get_project(api_key)
# print(new.catch_result(tasks,'yes'))
# print(new.catch_result(projects))
# print(new.catch_result(customer))


# working_hours_start = "23:00:00"#input ("Podaj o ktorej zaczynasz prace eg 07:00:00")
# working_hours_end = "07:00:00"#input ("Podaj o ktorej konczysz prace eg 15:00:00")
# start = "2019-02-04"#input(" Podaj date od ktorej zaczynasz zmiane eg 2019-02-02")
# end = "2019-02-04"#input(" Podaj date koncowa eg 2019-02-05")
# print(new.set_new_record(api_key,start,end,working_hours_start,working_hours_end))
#





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

