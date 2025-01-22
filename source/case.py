from source.functions import *

class Case:
    def __init__(self, data={}, data_by_user={}, metadata={}):
        if len(data) < 1:
            self.data, self.data_by_user, self.metadata = make_dummy_case()
        else:
            self.data = data
            self.data_by_user = data_by_user
            self.metadata = metadata

    def beregn_straf(self):
        pass
    
    def get_case_name(self):
        return self.data['case_name']

    def set_navn(self, navn=''):
        self.data['navn'] = navn
        self.data_by_user['navn'] = True
    
    def set_cpr(self, cpr=''):
        self.data['cpr'] = cpr
        self.data_by_user['cpr'] = True

    def set_fraktid(self, fraktid=False):
        self.data['fraktid'] = fraktid
        self.data_by_user['fraktid'] = True

    def update(self, data):
        for key, val in data.items():
            self.data[key] = val
            self.data_by_user[key] = True

    def data_to_dict(self):
        data_dict = {
            'data': self.data,
            'data_by_user': self.data_by_user,
            'metadata': self.metadata
        }
        return data_dict
    
