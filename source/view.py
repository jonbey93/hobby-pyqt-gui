import source.resources.qrc_resources
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from source.widgets import *
from source.functions import * 

class View(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PrisonTime")
        #self.setGeometry(600, 300, 550, 600)

        self.case_widget = self.CaseWidget()
        self.toolbar = self.ToolBarWidget()
        self.tabs_widget = self.TabsWidget()
        self.output_textbox = self.OutputTextBox('')
        
        self.layout = QGridLayout()  # row, column, rowSpan, columnSpan
        self.layout.addWidget(self.case_widget, 2, 0, 12, 2, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.toolbar, 0, 0, 2, 8, alignment=Qt.AlignTop)
        self.layout.addWidget(self.tabs_widget, 2, 2, 6, 6)
        self.layout.addWidget(self.output_textbox, 8, 2, 6, 6, alignment=Qt.AlignBottom)
        self.setLayout(self.layout)
    
    
    def CaseWidget(self):
        case_widget = QWidget()
        case_widget.setMinimumWidth(150)
        case_widget.setMaximumWidth(300)
        case_widget.setObjectName("case_widget")
        case_widget.setStyleSheet("""
            #case_widget {
                border: 1px solid white;
                border-radius: 8px;                           
            }
        """)

        title = QLabel('Sager')
        title.setAlignment(Qt.AlignHCenter)
        title.setStyleSheet("font: bold 14pt 'Verdana';")

        self.case_list_empty_label = QLabel('Ingen åbne sager')
        self.case_list_empty_label.setAlignment(Qt.AlignHCenter)
        self.case_list_empty_label.setStyleSheet("""
                                                 color: grey;
                                                 font: 10pt 'Verdana';
                                                 """)
        self.case_list_empty_label.hide()

        self.case_list = CaseList()
        

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addItem(QSpacerItem(0, 19, QSizePolicy.Minimum, QSizePolicy.Fixed))
        layout.addWidget(title)
        layout.addItem(QSpacerItem(0, 5, QSizePolicy.Minimum, QSizePolicy.Fixed))
        layout.addWidget(self.case_list_empty_label)
        layout.addWidget(self.case_list)

        case_widget.setLayout(layout)

        return case_widget
        

    def ToolBarWidget(self):
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)

        self.new_case_action = QAction("Ny sag (Ctrl+N)", self)
        self.open_case_action = QAction("Åben sag (Ctrl+O)", self)
        self.save_case_action = QAction("Gem sag (Ctrl+S)", self)
        self.close_case_action =QAction("Luk sag", self)
        self.del_case_action = QAction("Slet sag", self)

        self.new_case_action.setIcon(QIcon(":newfile-white.svg"))
        self.open_case_action.setIcon(QIcon(":open-white.svg"))
        self.save_case_action.setIcon(QIcon(":save-white.svg"))
        self.close_case_action.setIcon(QIcon(":closefile-white.svg"))
        self.del_case_action.setIcon(QIcon(":delfile-white.svg"))

        self.new_case_action.setShortcut("Ctrl+N")
        self.open_case_action.setShortcut("Ctrl+O")
        self.save_case_action.setShortcut("Ctrl+S")

        toolbar.addAction(self.new_case_action)
        toolbar.addAction(self.open_case_action)
        toolbar.addAction(self.save_case_action)
        toolbar.addAction(self.close_case_action)
        toolbar.addAction(self.del_case_action)

        return toolbar


    def TabsWidget(self):
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.North)
        tabs.setFixedHeight(400)
        tabs.setMinimumWidth(600)
        tabs.setContentsMargins(0, 0, 0, 0)
        tabs.setStyleSheet(load_stylesheet('tabs_styles.qss'))

        navn_validator = QRegularExpressionValidator(QRegularExpression(r"[^\d\W][\p{L}\-\'\` ]*"), self)
        cpr_validator = QRegularExpressionValidator(QRegularExpression(r"\d{6}-\d{4}"), self)

        ## TAB 1 ##
        personTab = QWidget()
        layout_main = QHBoxLayout()
        layout_left = QVBoxLayout()
        layout_right = QVBoxLayout()

        # left side
        self.navn_line = LineEdit("Navn", "", navn_validator)
        self.cpr_line = LineEdit("CPR-nummer", "", cpr_validator)

        layout_left.addWidget(self.navn_line)
        layout_left.addWidget(self.cpr_line)

        layout_left.setContentsMargins(0, 0, 0, 0)
        layout_left.setSpacing(0)
        layout_left.setAlignment(Qt.AlignTop)
        layout_main.addLayout(layout_left)

        # right side
        self.case_no_line = LineEdit("Sagsnummer", "")
        self.client_no_line = LineEdit("Klientnummer", "")

        layout_right.addWidget(self.case_no_line)
        layout_right.addWidget(self.client_no_line)

        layout_right.setContentsMargins(0, 0, 0, 0)
        layout_right.setSpacing(0)
        layout_right.setAlignment(Qt.AlignTop)
        layout_main.addLayout(layout_right)
        
        layout_main.setAlignment(Qt.AlignTop)
        personTab.setLayout(layout_main)

        ## TAB 2 ##
        tidlForseTab = QWidget()
        layout = QVBoxLayout()

        self.fraktid_box = CheckBox("Sket i frakendelsestiden")
        
        layout.addWidget(self.fraktid_box)

        layout.setAlignment(Qt.AlignTop)
        tidlForseTab.setLayout(layout)

        tabs.addTab(personTab, "Personoplysninger")
        tabs.addTab(tidlForseTab, "Tidl. Forseelser")

        ## TAB BORDER ##
        outer_widget = QWidget()
        outer_widget.setObjectName("outer_widget")

        self.tabs_label = QLabel('unavngivet')
        self.tabs_label.setAlignment(Qt.AlignHCenter)
        self.tabs_label.setStyleSheet("font: bold 14pt 'Verdana';")
        
        outer_layout = QVBoxLayout(outer_widget)
        outer_layout.setContentsMargins(10, 0, 10, 0) 
        outer_layout.addItem(QSpacerItem(0, 19, QSizePolicy.Minimum, QSizePolicy.Fixed))
        outer_layout.addWidget(self.tabs_label)
        outer_layout.addItem(QSpacerItem(0, 11, QSizePolicy.Minimum, QSizePolicy.Fixed))
        outer_layout.addWidget(tabs)
        outer_widget.setStyleSheet("""
            #outer_widget {
                border: 1px solid white;
                border-radius: 8px;
            }
        """)
        return outer_widget


    def OutputTextBox(self, welcome_text=''):
        output_text_box = QTextEdit(self)
        output_text_box.setFixedHeight(150)
        output_text_box.setContentsMargins(0, 0, 0, 0)
        output_text_box.setReadOnly(True)
        output_text_box.setText(welcome_text)
        output_text_box.setStyleSheet("""
            QTextEdit {
                color: white; 
                border: 1px solid white;
                background: light-grey;
            }
        """)

        self.output_text_box = output_text_box
        return output_text_box
    

    def SaveFileDialog(self, default_name=""):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Gem",
            default_name,
            "JSON Files (*.json);;All Files (*)",
            options=options
        )
        return file_path, _


    def OpenFileDialog(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Indlæs",
            "",
            "JSON Files (*.json);;All Files (*)",
            options=options
        )
        return file_path, _