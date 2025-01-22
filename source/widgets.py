from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from source.functions import *


class CaseList(QListWidget):
    actionSelected = pyqtSignal(str, object)

    def __init__(self):
        super().__init__()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        self.setStyleSheet(load_stylesheet('case_list_styles.qss'))
        self.cases = []

    def update_list(self, case_names):
        self.clear()
        self.cases = []
        if isinstance(case_names, str):
            case_names = [case_names]
        for case in case_names:
            if not case == 'unavngivet':
                self.addItem(case)
                self.cases.append(case)
            

    def add_case(self, case_names):
        if isinstance(case_names, str):
            case_names = [case_names]
        for case in case_names:
            if case not in self.cases:
                self.addItem(case)
                self.cases.append(case)

    def get_items(self):
        return [self.items(i).text() for i in range(self.count())]
    
    def select_case(self, case_name):
        for i in range(self.count()):
            item = self.item(i)
            if item.text() == case_name:
                self.setCurrentItem(item)
                self.update()
                break

    def show_context_menu(self, position):
        item = self.itemAt(position)
        if item:
            context_menu = QMenu()
            context_menu.setStyleSheet("""QMenu {
                                       color: white;
                                       background-color: light-grey;
                                       border: 2px solid black;
                                       border-radius: 8px;
                                       }
                                       """)

            open_action = context_menu.addAction("Åben")
            save_action = context_menu.addAction("Gem")
            delete_action = context_menu.addAction("Slet")

            open_action.triggered.connect(lambda: self.actionSelected.emit("itemOpen", item))
            save_action.triggered.connect(lambda: self.actionSelected.emit("itemSave", item))
            delete_action.triggered.connect(lambda: self.actionSelected.emit("itemDelete", item))
            
            context_menu.exec_(self.mapToGlobal(position))

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            item = self.itemAt(event.pos())
            if not item:
                self.clearSelection()
            return
        super().mousePressEvent(event)

    def bind_to(self, callback):
        self.itemClicked.connect(lambda item: callback("itemClicked", item))
        self.actionSelected.connect(lambda action, item: callback(action, item))  


class LineEdit(QWidget):
    def __init__(self, title='', placeholder='', validator=None):
        super().__init__()

        title = QLabel(title, self)
        self.line_edit = QLineEdit(self)
        self.indicator = Indicator(self)

        self.line_edit.setPlaceholderText(placeholder)
        self.line_edit.setFixedSize(200, 25)
        self.line_edit.setStyleSheet(load_stylesheet('line_edit_styles.qss'))

        self.line_edit.setValidator(validator)

        indicator_layout = QHBoxLayout()
        indicator_layout.addWidget(self.line_edit)
        indicator_layout.addWidget(self.indicator.indicator, alignment=Qt.AlignLeft)
        indicator_layout.setSpacing(5)  

        main_layout = QVBoxLayout()
        main_layout.addWidget(title)
        main_layout.addLayout(indicator_layout)
        main_layout.setSpacing(2)
        main_layout.setContentsMargins(0, 10, 0, 10)

        self.setLayout(main_layout)

    def get_text(self):
        input = self.line_edit.text()
        return input

    def set_text(self, text):
        self.line_edit.setText(text)

    def block_signals(self, bool=False):
        self.line_edit.blockSignals(bool)

    def bind_to(self, callback):
        self.line_edit.textChanged.connect(lambda: callback("textChanged"))
        self.line_edit.returnPressed.connect(lambda: callback("returnPressed"))


class DropDownMenu(QWidget):
    def __init__(self, title='', placeholder='', options=[]):
        super().__init__()

        self.options = options

        title = QLabel(title, self)
        self.drop_down_menu = QComboBox(self)
        self.indicator = Indicator(self)
        
        self.drop_down_menu.addItem(placeholder)
        self.drop_down_menu.addItems(options)
        self.drop_down_menu.setFixedSize(200, 25)

        indicator_layout = QHBoxLayout()
        indicator_layout.addWidget(self.drop_down_menu)
        indicator_layout.addWidget(self.indicator.indicator, alignment=Qt.AlignLeft)
        indicator_layout.setSpacing(5)  

        main_layout = QVBoxLayout()
        main_layout.addWidget(title)
        main_layout.addLayout(indicator_layout)

        self.setLayout(main_layout)

    def get_selection(self):
        selection = self.options[self.drop_down_menu.currentIndex()-1]
        return selection

    def bind_to(self, callback):
        self.drop_down_menu.currentIndexChanged.connect(lambda: callback('currentIndexChanged'))


class CheckBox(QWidget):
    def __init__(self, title=''):
        super().__init__()

        title = QLabel(title, self)
        self.checkbox = QCheckBox(self)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(self.checkbox)
        layout.setContentsMargins(0, 10, 0, 10)

        self.setLayout(layout)

    def get_state(self):
        state = self.checkbox.isChecked()
        return state

    def set_state(self, state):
        self.checkbox.setChecked(state)

    def block_signal(self, bool):
        self.checkbox.blockSignals(bool)

    def bind_to(self, callback):
        self.checkbox.stateChanged.connect(lambda: callback('stateChanged'))
    

class Indicator(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.indicator = QLabel(self)

        self.indicator.setFixedSize(12, 12)

        self.indicator.setStyleSheet("""QLabel
                                     {background-color : lightgray;
                                     border-color : black;
                                     border-width : 1px;
                                     border-style : solid;
                                     border-radius : 5px}""")

    def green(self):
        self.indicator.setStyleSheet("""QLabel
                                     {background-color : lightgreen;
                                     border-color : black;
                                     border-width : 1px;
                                     border-style : solid;
                                     border-radius : 6px}""")

    def yellow(self):
        self.indicator.setStyleSheet("""QLabel
                                     {background-color : yellow;
                                     border-color : black;
                                     border-width : 1px;
                                     border-style : solid;
                                     border-radius : 6px}""") 

    def grey(self):
        self.indicator.setStyleSheet("""QLabel
                                     {background-color : lightgrey;
                                     border-color : black;
                                     border-width : 1px;
                                     border-style : solid;
                                     border-radius : 6px}""")


class UserDialog(QDialog):
    def __init__(self, title='', dialog=''):
        super().__init__()

        self.user_input = None

        layout = QVBoxLayout()
        self.setWindowTitle(title)
        self.setGeometry(750, 450, 300, 120)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        label = QLabel(dialog, self)
        layout.addWidget(label)
        
        self.line_edit = QLineEdit(self)
        self.line_edit.returnPressed.connect(self.on_confirm)
        layout.addWidget(self.line_edit)

        button_layout = QHBoxLayout()

        self.confirm_button = QPushButton("Bekræft", self)
        self.confirm_button.clicked.connect(self.on_confirm)
        button_layout.addWidget(self.confirm_button)

        self.cancel_button = QPushButton("Anuller", self)
        self.cancel_button.clicked.connect(self.on_confirm)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)

    def on_confirm(self):
        self.user_input = self.line_edit.text()
        self.accept()

    def get_user_input(self):
        return self.user_input


class UserConfirmDialog(QDialog):
    def __init__(self, title='', dialog='', accept_text='Ok', reject_text='Cancel'):
        super().__init__()

        layout = QVBoxLayout()
        self.setWindowTitle(title)
        self.setGeometry(750, 450, 300, 120)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        label = QLabel(dialog, self)

        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        
        accept_button = self.buttonBox.button(QDialogButtonBox.Ok)
        reject_button = self.buttonBox.button(QDialogButtonBox.Cancel)

        accept_button.setText(accept_text)
        reject_button.setText(reject_text)

        layout.addWidget(label)
        layout.addWidget(self.buttonBox)

        self.setLayout(layout)