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
        value_list = [project_value,task_value,project_name,task_name]
        return value_list

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
        cfg_recovery = '''; cfg.ini
        [project_value]
        projectid = 2
        taskid = 12
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