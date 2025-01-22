import sys, os

def load_stylesheet(file_name):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    stylesheet_path = os.path.join(base_path, "stylesheets", file_name)
    with open(stylesheet_path, "r") as f:
        return f.read()


def find_json_files_in_folder(folder_path):
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        return []
    json_files = [file for file in os.listdir(folder_path) if file.endswith('.json')]
    return json_files


def make_dummy_case():
    data = {
        'case_name': 'unavngivet',
        'navn': '',
        'cpr': '',
        'fraktid': False,
    }
    data_by_user = {
        'case_name': False,
        'navn': False,
        'cpr': False,
        'fraktid': False,
    }
    metadata = {
        'file_path': '',
        'last-edit': '',
    }
    return data, data_by_user, metadata