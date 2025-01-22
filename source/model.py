import json, copy
from source.functions import *
from source.case import Case

class Model:
    def __init__(self):
        self.cases = {}
        self.current_case = Case()

    def create_new_case(self, case_name='unavngivet'):
        new_case = Case()
        new_case.data['case_name'] = case_name
        self.cases[case_name] = new_case

    def get_case(self, case_name):
        return self.cases[case_name]
    
    def set_current_case(self, case):
        if type(case) == str:
            self.current_case = self.cases[case]
        elif type(case) == Case:
            self.current_case = case

    def get_current_case_name(self):
        return self.current_case.data['case_name']

    def get_case_names(self):
        return list(self.cases.keys())

    def delete_case(self, case_name):
        if case_name in self.cases.keys():
            del self.cases[case_name]

    def load_case(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        case = Case(data['data'], data['data_by_user'], data['metadata'])
        self.cases[case.get_case_name()] = case
        if not self.get_current_case_name() == 'unavngivet':
            self.cases[self.get_current_case_name()] = copy.deepcopy(self.current_case)
        self.current_case = case

    def save_case(self, file_path, case_name):
        with open(file_path, 'w') as file:
            json.dump(self.cases[case_name].data_to_dict(), file, indent=4)  

    # havent been tested
    def save_all_cases(self, file_path_root):
        for case_name in self.cases.keys():
            with open(file_path_root + case_name, 'w') as file:
                json.dump(self.cases[case_name].data_to_dict(), file, indent=4)

    def save_current_case(self, file_path):
        self.current_case.metadata['file_path'] = file_path
        with open(file_path, 'w') as file:
            json.dump(self.current_case.data_to_dict(), file, indent=4)        
