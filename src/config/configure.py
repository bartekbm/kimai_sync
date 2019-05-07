from configparser import ConfigParser
from pathlib import Path
import os
absFilePath = os.path.abspath(__file__)
fileDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.dirname(fileDir)
parentDirLvlDown = os.path.dirname(parentDir)

file_cfg_path = os.path.join(parentDirLvlDown, 'cfg.ini')
ico=os.path.join(parentDirLvlDown, 'favicon.ico')
file_cfg = Path(file_cfg_path)


class Configuration:
    parser = ConfigParser()
    def __init__(self):
        pass

    def readFromConfig(self):
        self.parser.read(file_cfg)
        project_value=self.parser.get('project_value','projectId')
        task_value=self.parser.get('project_value','taskId')
        project_name=self.parser.get('project_name','project')
        task_name=self.parser.get('project_name','task')
        shift_a=self.parser.get('hours','a').split(',')
        shift_b = self.parser.get('hours', 'b').split(',')
        shift_c = self.parser.get('hours', 'c').split(',')
        shift_cc = self.parser.get('hours', 'cc').split(',')
        shift_w= self.parser.get('hours', 'w').split(',')
        shift_random = self.parser.get('hours', 'random').split(',')
        web=self.parser.get('web','site')
        value_list = {
            "procject_value":project_value,
            "task_value":task_value,
            "project_name":project_name,
            "task_name":task_name,
            "shift_a":shift_a,
            "shift_b": shift_b,
            "shift_c": shift_c,
            "shift_cc": shift_cc,
            "shift_w": shift_w,
            "shift_random": shift_random,
            "website":web,
            "cfg":file_cfg
        }
        return value_list


    def saveToFile(self,**kwargs):
        self.parser.read(file_cfg)
        for key, value in kwargs.items():
            if key == 'project_value':
                self.parser['project_value']['projectId'] = value
            elif key == 'taskId_value':
                self.parser['project_value']['taskId'] = value
            elif key == 'project_name':
                self.parser['project_name']['project'] = value
            elif key == 'taskId_name':
                self.parser['project_name']['task'] = value
            elif key == 'shift_a':
                self.parser.set('hours','a',value=value)
            elif key == 'shift_b':
                self.parser.set('hours','b',value=value)
            elif key == 'shift_c':
                self.parser.set('hours','c',value=value)
            elif key == 'shift_cc':
                self.parser.set('hours','cc',value=value)
            elif key == 'shift_w':
                self.parser.set('hours','w',value=value)
            elif key == 'shift_random':
                self.parser.set('hours','random',value=value)



        with open(file_cfg, 'w') as configfile:
            self.parser.write(configfile)

    def fileGlobal(self):
        return ico
    def checkRecoveryCfg(self):
        cfg_recovery = '''
[project_value]
projectid = 57
taskid = 17

[project_name]
project = !P000_WsparcieProdukcji (DDUIT_US_OPER)
task = !!!_Praca operacyjna
        
[hours]
a = 07:00,15:00
b = 15:00,23:00
c = 23:00,07:00
cc = 19:00,07:00
w = 07:00,19:00
random = 06:00,23:00

[web]
site= http://192.168.0.164/kimai/core/json.php'''

        if file_cfg.is_file() == False:
            with open(
                    file_cfg,
                    'w') as f:
                f.write(cfg_recovery)
