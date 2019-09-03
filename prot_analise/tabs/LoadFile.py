from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget, QFileDialog, QTextEdit, QVBoxLayout, QGroupBox

global licznik_go
licznik_go = 1


class LoadFile(QWidget):
    def __init__(self, fasta):
        super().__init__()

        self.path = ""
        self.fasta = fasta
        self.proteins = {}
        name = QLabel("File Source: ")
        self.nameEdit = QTextEdit(self)
        self.nameEdit.setMaximumHeight(30)
        self.nameEdit.setText("../examples/clustry_H.csv")

        selctGroup = QGroupBox("")
        selctGroup2 = QGroupBox("")

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

        layout2 = QHBoxLayout()
        button3 = QtWidgets.QPushButton("Download datas from uniprot")
        button3.clicked.connect(self.get_group_taxonomy)

        checkGroup3 = QGroupBox("Get information about proteins from file (not implemented yet):")

        layout3 = QHBoxLayout()
        name = QLabel("XML file source of protein: ")
        self.nameEdit2 = QTextEdit(self)
        self.nameEdit2.setMaximumHeight(30)
        button4 = QtWidgets.QPushButton("Get File")
        button4.clicked.connect(self.get_path)
        button5 = QtWidgets.QPushButton("Load File")
        button5.clicked.connect(self.source_datas)

        layout3.addWidget(name)
        layout3.addWidget(self.nameEdit2)
        layout3.addWidget(button4)
        layout3.addWidget(button5)
        checkGroup3.setLayout(layout3)

        layout2.addWidget(button3)

        self.ended = QLabel("No lenghts and taxonomic")

        layout2.addWidget(self.ended)

        selctGroup.setLayout(layout)
        selctGroup2.setLayout(layout2)

        mainLayout.addWidget(selctGroup)
        mainLayout.addWidget(checkGroup3)
        mainLayout.addWidget(selctGroup2)

        self.setLayout(mainLayout)

    def get_path(self):
        self.update_tab()
        filename = QFileDialog.getOpenFileName(self, "Open File", "./")
        if filename[0]:
            self.nameEdit.setText(filename[0])
        self.update()

    def update_tab(self):
        self.proteins = self.fasta.proteins
        self.species = self.fasta.species
        self.cells = self.fasta.cells
        self.path = self.fasta.path
        self.lenths = self.fasta.lenths
        self.kingdom = self.fasta.kingdom

    def load_datas(self):
        self.update_tab()
        self.get_path()
        self.update()

    def source_datas(self):
        # todo: tu jest coś dziwnego
        self.path = self.nameEdit.toPlainText()
        if self.path:
            # todo: dodać okienko lub napis - brak takiego pliku
            # todo: dodać sprawdzanie czy wlaściwy format plików
            self.fasta.get_path(self.path)

    def get_group_taxonomy(self):
        missing = self.fasta.get_group_taxonomy()
        if len(missing) == 0:
            self.ended.setText("Finded lenths and taxonomies")
        else:
            self.ended.setText("Finded lenths and taxonomies, missed " + str(len(missing)) + " proteins")
            print(missing)
