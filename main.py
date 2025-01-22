import sys, qdarktheme
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from source.model import Model
from source.view import View
from source.presenter import Presenter
from source.functions import *

def main():
    app = QApplication(sys.argv)

    qdarktheme.setup_theme()
    app.setFont(QFont("Verdana", 10))

    model = Model()
    view = View()
    presenter = Presenter(view, model)

    view.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()