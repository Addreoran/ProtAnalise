from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget, QFileDialog, QTextEdit, QVBoxLayout, QGroupBox


class LoadFile(QWidget):
    def __init__(self, fasta):
        super().__init__()

        self.path = ""
        self.path_database = ""
        self.fasta = fasta
        self.proteins = dict
        name = QLabel("File Source: ")
        self.nameEdit = QTextEdit(self)
        self.nameEdit.setMaximumHeight(30)
        self.nameEdit.setText("../examples/clustry_H.csv")

        selctGroup = QGroupBox("")
        mainLayout = QVBoxLayout()

        layout = QHBoxLayout()
        layout.addWidget(name)
        layout.addWidget(self.nameEdit)
        button1 = QtWidgets.QPushButton("Load File")
        button1.clicked.connect(self.source_datas)
        button2 = QtWidgets.QPushButton("Get File")
        button2.clicked.connect(self.get_path)
        layout.addWidget(button2)
        layout.addWidget(button1)

        button3 = QtWidgets.QPushButton("Download data from UniprotKB")
        button3.clicked.connect(self.get_group_taxonomy)

        self.checkGroup3 = QGroupBox("Get information about proteins from file (not implemented jet):")

        layout3 = QHBoxLayout()
        name = QLabel("XML file source of protein: ")
        self.nameEdit2 = QTextEdit(self)
        self.nameEdit2.setMaximumHeight(30)
        self.nameEdit2.setText("../examples/clustry_H.xml")
        button4 = QtWidgets.QPushButton("Get File")
        button4.clicked.connect(self.get_path_database)
        button5 = QtWidgets.QPushButton("Load File")
        button5.clicked.connect(self.source_data_UniprotKB)

        layout3.addWidget(name)
        layout3.addWidget(self.nameEdit2)
        layout3.addWidget(button4)
        layout3.addWidget(button5)
        self.checkGroup3.setLayout(layout3)
        self.checkGroup3.hide()

        self.selctGroup2 = QGroupBox("")
        layout2 = QHBoxLayout()
        layout2.addWidget(button3)
        self.ended = QLabel("No lengths and taxonomic.")
        layout2.addWidget(self.ended)
        self.selctGroup2.setLayout(layout2)
        self.selctGroup2.hide()

        selctGroup.setLayout(layout)

        mainLayout.addWidget(selctGroup)
        mainLayout.addWidget(self.checkGroup3)
        mainLayout.addWidget(self.selctGroup2)

        self.setLayout(mainLayout)

    def get_path(self):
        self.update_tab()
        filename = QFileDialog.getOpenFileName(self, "Open File", "./")
        if filename[0]:
            self.nameEdit.setText(filename[0])
        self.update()

    def get_path_database(self):
        self.update_tab()
        filename = QFileDialog.getOpenFileName(self, "Open File", "./")
        if filename[0]:
            self.nameEdit2.setText(filename[0])
        self.update()

    def update_tab(self):
        self.proteins = self.fasta.proteins
        self.species = self.fasta.species
        self.cells = self.fasta.cells
        self.path = self.fasta.path
        self.lengths = self.fasta.lengths
        self.kingdom = self.fasta.kingdom

    def load_datas(self):
        self.update_tab()
        self.get_path()
        self.update()

    def source_datas(self):
        self.path = self.nameEdit.toPlainText()
        if self.path:
            self.fasta.get_path(self.path)
            self.update_tab()
            if len(self.proteins.items()) > 0:
                self.selctGroup2.show()
                self.checkGroup3.show()

    def source_data_UniprotKB(self):
        self.path_database = self.nameEdit2.toPlainText()
        if self.path_database:
            self.fasta.get_data_database(self.path_database)
            self.ended.setText("Found lengths and taxonomies. No information about missing.")

    def get_group_taxonomy(self):
        missing = self.fasta.get_group_taxonomy()
        if len(missing) == 0:
            self.ended.setText("Found lengths and taxonomies.")
        else:
            self.ended.setText("Found lengths and taxonomies, missed " + str(len(missing)) + " proteins.")
            print(missing)
