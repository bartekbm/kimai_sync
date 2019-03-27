from configparser import ConfigParser
from pathlib import Path
file_cfg = Path('C:/Users/bartosz/OneDrive/programowanie/private_projects_python/kimai_xls_sync/src/config/cfg.ini')

# parser.read('cfg.ini')
# test_pars = parser.get('project_value','projectId')
# print(test_pars)
# parser['project_value']['projectId'] = '90328490832098429083492348902348'
# with open('cfg.ini', 'w') as configfile:    # save
#     parser.write(configfile)


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
            "shift_random": shift_random
        }
        return value_list
        #return dict

    def saveToFile(self,p=None,t=None,pn=None,tn=None):
        self.parser.read(file_cfg)
        if p !=None:
            self.parser['project_value']['projectId'] = p
        if t !=None:
            self.parser['project_value']['taskId'] = t
        if pn !=None:
            self.parser['project_name']['project'] = pn
        if tn !=None:
            self.parser['project_name']['task'] = tn

        with open(file_cfg, 'w') as configfile:
            self.parser.write(configfile)
    def checkRecoveryCfg(self):
        cfg_recovery = ''';
        [project_value]
        projectid = 2
        taskid = 4
        
        [project_name]
        project = !P000_WsparcieProdukcji
        task = !!!_OP-opieka na dziecko
        
        [hours]
        a= ["7:00","15:00"]
        b_start=15:00
        b_end=23:00
        c_start=23:00
        c_end=07:00
        cc_start=19:00
        cc_end=07:00
        w_start=07:00
        w_end=19:00
        
        [user]
        username = bartek
        '''

        if file_cfg.is_file() == False:
            with open(
                    'C:/Users/bartosz/OneDrive/programowanie/private_projects_python/kimai_xls_sync/src/config/cfg.ini',
                    'w') as f:
                f.write(cfg_recovery)

# a = Configuration()
#
# a.saveToFile(None,"15")