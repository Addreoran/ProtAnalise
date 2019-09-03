import multiprocessing
import sys
from PyQt5.QtWidgets import QApplication, QDialog, QTabWidget, QVBoxLayout
from scripts.MenageData import AllData
from tabs.LoadFasta import LoadFasta
from tabs.LoadFile import LoadFile


class Window(QDialog):
    def __init__(self):
        super().__init__()
        self.title = "Protein Analiser"
        self.top = 100
        self.left = 100
        self.width = 600
        self.height = 500
        self.InitWIndow()

    def InitWIndow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        tabWidget = QTabWidget()
        self.all_datas = AllData()
        load = LoadFile(self.all_datas)
        tabWidget.addTab(load, "Load File")
        tabWidget.addTab(LoadFasta(self.all_datas), "Data")
        vbox = QVBoxLayout()
        vbox.addWidget(tabWidget)
        self.setLayout(vbox)
        self.show()


if __name__ == '__main__':
    if sys.platform.startswith('win'):
        # On Windows calling this function is necessary.
        multiprocessing.freeze_support()
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())
