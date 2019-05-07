class ReportsHandling():
    def __init__(self,json_data):
        self.json_data=json_data

    def test(self):
        print(len(self.json_data))
        print(self.json_data[0]['start'])

