import os
from source.widgets import *
from source.functions import *

class Presenter:
    def __init__(self, view, model):
        self.view = view
        self.model = model

        self.user_path = f'C:\Python\straffeberegning\PrisonTimeGUI'

        # case list
        self.view.case_list.bind_to(self.handle_case_list)

        # toolbar
        self.view.new_case_action.triggered.connect(self.handle_new_case_action)
        self.view.open_case_action.triggered.connect(self.handle_open_case_action)
        self.view.save_case_action.triggered.connect(self.handle_save_case_action)
        self.view.close_case_action.triggered.connect(self.handle_close_case_action)
        self.view.del_case_action.triggered.connect(self.handle_del_case_action)

        # tab1
        self.view.navn_line.bind_to(self.handle_navn_line)
        self.view.cpr_line.bind_to(self.handle_cpr_line)

        # tab2
        self.view.fraktid_box.bind_to(self.handle_fraktid_box)


        # initiate
        self.handle_case_list('__startup__')
        self.update_tabs('__startup__')

    
    # case list actions
    def handle_case_list(self, event_type, item=None):
        if event_type == 'itemClicked':
            self.model.set_current_case(item.text())
            self.update_tabs()
            self.view.output_textbox.append(f"({self.model.get_current_case_name()})")
        elif event_type == '__startup__':
            case_files = find_json_files_in_folder(self.user_path)
            for case_file in case_files:
                self.model.load_case(case_file)
            self.view.case_list.add_case(self.model.get_case_names())
            self.view.case_list.select_case(self.model.get_current_case_name())
            if self.view.case_list.count() < 1:
                self.view.case_list_empty_label.show()
            else:
                self.update_tabs()
        elif event_type == '__update__':
            self.view.case_list.update_list(self.model.get_case_names())
            if self.view.case_list.count() < 1:
                self.view.case_list_empty_label.show()
            else:
                self.view.case_list_empty_label.hide()
        elif event_type == 'itemOpen':
            self.handle_case_list('itemClicked', item)
        elif event_type == 'itemSave':
            self.model.set_current_case(item.text())
            self.handle_save_case_action()
        elif event_type == 'itemDelete':
            self.model.set_current_case(item.text())
            self.handle_del_case_action()


    # toolbar actions
    def handle_new_case_action(self):
        dialog = UserDialog(title='Ny sag', dialog='Indtast navn på ny sag:')
        if dialog.exec_() == QDialog.Accepted:
            case_name = dialog.get_user_input()
            if case_name == "unavngivet":
                self.view.output_textbox.append("-- Navn må ikke være \"unavngivet\" --")
                return
        else:
            return
        if case_name not in self.model.cases.keys():
            self.model.create_new_case(case_name)
            self.model.current_case = self.model.cases[case_name]
            self.view.case_list.add_case(self.model.get_current_case_name())
            self.handle_case_list('__update__')
            self.view.case_list.select_case(self.model.get_current_case_name())
            self.update_tabs()
        else:
            self.view.output_textbox.append(f"({case_name}) eksisterer allerede.")

    def handle_open_case_action(self):
        file_path, _ = self.view.OpenFileDialog()
        if file_path:
            self.model.load_case(file_path)
            self.handle_case_list('__update__')
            self.view.case_list.select_case(self.model.get_current_case_name())
            self.update_tabs()
            self.view.output_textbox.append(f"({self.model.get_current_case_name()})  Sag åbnet ")

    def handle_save_case_action(self):
        file_path = self.model.current_case.metadata['file_path']
        if self.model.current_case.data['case_name'] == 'unavngivet':
            dialog = UserDialog(title='Gem Sag', dialog='Indtast sagsnavn:')
            while True:
                if dialog.exec_() == QDialog.Accepted:
                    case_name = dialog.get_user_input()
                    if case_name == "unavngivet":
                        QMessageBox.warning(
                            None,
                            "Ugyldigt Navn",
                            f"Navn må ikke være '{case_name}'. Prøv venligst igen."
                        )
                    else:
                        break
                else:
                    return
        else:
            case_name = self.model.get_current_case_name()
        if not os.path.exists(file_path):
            file_path, _ = self.view.SaveFileDialog(default_name=case_name)
            if file_path:
                self.model.create_new_case(case_name)
                self.model.current_case = self.model.cases[case_name]
                self.model.current_case.data['case_name'] = case_name
                self.model.current_case.data_by_user['case_name'] = True
                self.model.current_case.update(self.get_current_input())
                self.model.current_case.metadata['file_path'] = file_path
                self.model.save_current_case(file_path)
                self.view.output_textbox.append(f"({self.model.get_current_case_name()})  Sag gemt under " + file_path)
                self.update_tabs('__save__')
        else:
            self.model.save_current_case(file_path)
            self.update_tabs('__save__')
            self.view.output_textbox.append(f"({self.model.get_current_case_name()})  Sag gemt under " + file_path)
        self.handle_case_list('__update__')
        self.view.case_list.select_case(self.model.get_current_case_name())

    def handle_close_case_action(self):
        case_name = self.model.get_current_case_name()
        if not case_name == 'unavngivet':
            dialog = UserConfirmDialog(title=f"Luk sag",
                                       dialog=f"Er du sikker på at du vil lukke {case_name}?",
                                       accept_text='Ja',
                                       reject_text='Nej')  
            if dialog.exec_() == QDialog.Accepted:
                case_names = self.model.get_case_names()
                case_pos = case_names.index(case_name)
                if len(case_names) > 1:
                    if case_pos > 0:
                        new_current_case = case_names[case_pos - 1]
                    elif case_pos < len(case_names):
                        new_current_case = case_names[case_pos + 1]
                    self.model.set_current_case(new_current_case)
                else:
                    self.model.create_new_case('unavngivet')
                    self.model.set_current_case('unavngivet')
                del self.model.cases[case_name]
                self.handle_case_list('__update__')
                self.view.case_list.select_case(self.model.get_current_case_name())
                self.update_tabs()
            else:
                return
        else:
            pass

    def handle_del_case_action(self):
        case_name = self.model.get_current_case_name()
        if not case_name == 'unavngivet':
            dialog = UserConfirmDialog(title=f"Slet sag",
                            dialog=f"Er du sikker på at du vile slette {case_name} fra din computer?",
                            accept_text='Ja',
                            reject_text='Nej')
            if dialog.exec_() == QDialog.Accepted:
                dialog = UserConfirmDialog(title=f"Slet sag",
                                        dialog=f"Er du helt sikker?",
                                        accept_text='Ja',
                                        reject_text='Nej')  
                if dialog.exec_() == QDialog.Accepted:
                    case_names = self.model.get_case_names()
                    case_pos = case_names.index(case_name)
                    if len(case_names) > 1:
                        if case_pos > 0:
                            new_current_case = case_names[case_pos - 1]
                        elif case_pos < len(case_names):
                            new_current_case = case_names[case_pos + 1]
                        self.model.set_current_case(new_current_case)
                    else:
                        self.model.create_new_case('unavngivet')
                        self.model.set_current_case('unavngivet')
                    file_path = self.model.cases[case_name].metadata['file_path']
                    try:
                        os.remove(file_path)
                        self.view.output_textbox.append(f"({case_name}) -- slettet --")
                    except Exception as e:
                        print(f"An error occurred: {e}")
                    del self.model.cases[case_name]
                    self.handle_case_list('__update__')
                    self.view.case_list.select_case(self.model.get_current_case_name())
                    self.update_tabs()
                else:
                    return
            else:
                return
        else:
            pass

    # tab user actions
    def handle_navn_line(self, event_type):
        input_text = self.view.navn_line.get_text()
        if event_type == 'textChanged':
            if not self.model.current_case.data_by_user['navn']:
                pass
            else:
                if input_text == self.model.current_case.data['navn']:
                    self.view.navn_line.indicator.green()
                else:
                    self.view.navn_line.indicator.yellow()
        elif event_type =='returnPressed':
            if input_text == '':
                if self.model.current_case.data['navn'] != input_text:
                    self.model.current_case.set_navn(input_text)
                    self.view.navn_line.indicator.grey()
                    self.view.output_textbox.append(f"({self.model.get_current_case_name()})  Navn: --slettet--")
            else:
                if self.model.current_case.data['navn'] != input_text:
                    self.model.current_case.set_navn(input_text)
                    self.view.navn_line.indicator.green()
                    self.view.output_textbox.append(f"({self.model.get_current_case_name()})  Navn: {self.model.current_case.data['navn']}")
        elif event_type == '__save__':
            self.model.current_case.data['navn'] = input_text
            self.view.navn_line.indicator.green()
        elif event_type == '__update__':
            self.view.navn_line.set_text(self.model.current_case.data['navn'])
            if self.model.current_case.data['navn']:
                self.view.navn_line.indicator.green()
            else:
                self.view.navn_line.indicator.grey()
        elif event_type == '__startup__':
            pass


    def handle_cpr_line(self, event_type):
        input_text = self.view.cpr_line.get_text()
        if event_type == 'textChanged':
            print('hej', input_text)
            cleaned_text = input_text.replace("-", "")
            if len(cleaned_text) > 6:
                formatted_text = f"{cleaned_text[:6]}-{cleaned_text[6:]}"
            else:
                formatted_text = cleaned_text
            self.view.cpr_line.block_signals(True)
            self.view.cpr_line.set_text(formatted_text)
            self.view.cpr_line.block_signals(False)
            if not self.model.current_case.data_by_user['cpr']:
                pass
            else:
                if input_text == self.model.current_case.data['cpr']:
                    self.view.cpr_line.indicator.green()
                else:
                    self.view.cpr_line.indicator.yellow()
        elif event_type =='returnPressed':
            if input_text == '':
                if self.model.current_case.data['cpr'] != input_text:
                    self.model.current_case.set_cpr(input_text)
                    self.view.cpr_line.indicator.grey()
                    self.view.output_textbox.append(f"({self.model.get_current_case_name()})  CPR: --slettet--")
            else:
                if self.model.current_case.data['cpr'] != input_text:
                    self.model.current_case.set_cpr(input_text)
                    self.view.cpr_line.indicator.green()
                    self.view.output_textbox.append(f"({self.model.get_current_case_name()})  CPR: {self.model.current_case.data['cpr']}")
        elif event_type == '__save__':
            self.model.current_case.data['cpr'] = input_text
            self.view.cpr_line.indicator.green()
        elif event_type == '__update__':
            self.view.cpr_line.set_text(self.model.current_case.data['cpr'])
            if self.model.current_case.data['cpr']:
                self.view.cpr_line.indicator.green()
            else:
                self.view.cpr_line.indicator.grey()
        elif event_type == '__startup__':
            pass


    def handle_fraktid_box(self, event_type):
        state = self.view.fraktid_box.get_state()
        if event_type == 'stateChanged':
            if state:
                self.model.current_case.set_fraktid(True)
                self.view.output_textbox.append(f"({self.model.get_current_case_name()})  Sket i frakendelsestiden: Ja")
            else:
                self.model.current_case.set_fraktid(False)
                self.view.output_textbox.append(f"({self.model.get_current_case_name()})  Sket i frakendelsestiden: Nej")
        elif event_type == '__save__':
            self.model.current_case.data['fraktid'] = state
        elif event_type == '__update__':
            self.view.fraktid_box.block_signal(True)
            self.view.fraktid_box.set_state(self.model.current_case.data['fraktid'])
            self.view.fraktid_box.block_signal(False)
        elif event_type == '__startup__':
            pass


    def handle_koen_menu(self, index):
        if index == 0:
            if self.model.koen_by_user:
                self.view.koen_menu.indicator.grey()
            else:
                pass
        else:
            koen = self.view.koen_menu.get_selection()
            if koen == self.model.koen:
                self.view.koen_menu.indicator.green()
            else:
                self.model.set_koen(koen)
                self.view.koen_menu.indicator.green()
                self.view.output_textbox.append(f"({self.model.get_current_case_name()})  Køn: {self.model.koen}")


    # auxiliary functions
    def get_current_input(self):
        data = {}
        data['navn'] = self.view.navn_line.get_text()
        data['cpr'] = self.view.cpr_line.get_text()
        data['fraktid'] = self.view.fraktid_box.get_state()
        return data
    

    def update_tabs(self, event_type='__update__'):
        self.handle_navn_line(event_type)
        self.handle_cpr_line(event_type)
        self.handle_fraktid_box(event_type)
        self.view.tabs_label.setText(self.model.get_current_case_name())