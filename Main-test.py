from ui_file import *


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)
        self.show()

        self.uiController = UiController()

        # self.setStyleSheet("background-color: #303030")
        #
        # # modifier la couleur du texte de l'application entiere en blanc
        # for label in self.findChildren(QWidget):
        #     label.setStyleSheet("background-color: #303030")
        #
        # # modifier le background du QTabWidget en noir
        # for tab in self.findChildren(QTabWidget):
        #     tab.setStyleSheet("background-color: #303030")


if __name__ == '__main__':
    app = QApplication()
    window = Main()
    app.exec()
