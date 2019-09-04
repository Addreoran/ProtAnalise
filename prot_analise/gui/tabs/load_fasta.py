from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget, QTextEdit, QComboBox, QHBoxLayout, QGroupBox

from prot_analise.scripts.region import Region


class LoadFasta(QWidget):
    def __init__(self, fasta):
        super().__init__()
        self.fasta = fasta
        self.go_grooup = ""
        self.path = ""
        self.proteins = {}
        self.lengths = {}
        self.species = {}
        name = QLabel("File: ")
        self.file = QTextEdit(self)
        self.combo = QComboBox()
        self.combo.currentTextChanged.connect(self.get_regions)
        self.combo_group = QComboBox()
        self.list = self.get_proteins()
        layout = QVBoxLayout()
        self.layout_combo = QHBoxLayout()
        checkGroup = QGroupBox()
        self.layout_combo.addWidget(self.combo)
        self.layout_combo.addWidget(self.combo_group)
        checkGroup.setLayout(self.layout_combo)
        layout.addWidget(checkGroup)
        layout.addWidget(name)
        layout.addWidget(self.file)
        self.loaded_protein = ""
        button2 = QtWidgets.QPushButton("Update protein")
        button2.clicked.connect(self.update_protein)
        layout.addWidget(button2)
        self.group = "UniprotId"
        self.combo_group.addItems(["", "UniprotId", "Species", "Groups of Taxonomy (Cellular)"])
        self.combo_group.currentTextChanged.connect(self.update_proteins)
        self.combo_group_go = ""
        self.go_by_anch = {}
        self.setLayout(layout)

    def set_lengths(self, lengths):
        self.lengths = lengths
        self.update()

    def source_datas(self):
        self.path = self.nameEdit.toPlainText()
        print(self.path)

    def get_proteins(self):
        return list(self.proteins.keys())

    def get_update(self):
        self.update_tab()
        self.proteins = self.fasta.proteins
        self.species = self.fasta.species
        all_regions = []
        for i in self.proteins.values():
            all_regions += list(i)
        all_proteins = []
        for region in self.species.items():
            all_proteins.append(region[0] + ", proteins:" + str(len(region[1])))
        self.combo.addItems(
            ["all, proteins:" + str(len(self.proteins.keys())) + ", regions:" + str(
                len(all_regions))] + all_proteins)
        self.loaded_protein = ""
        self.update()

    def get_regions(self):
        self.update_tab()
        self.loaded_protein = str(self.combo.currentText()).split(",")[0]
        text = self.fasta.get_text(self.combo_group.currentText(), self.loaded_protein)
        self.file.setText(text)
        self.update()

    def get_region_by_seq(self, list, seq, begin, end):
        for sequence in list:
            if sequence.sequence == seq and sequence.begin == begin and sequence.end == end:
                return sequence

    def update_protein(self):
        self.update_tab()
        if self.combo_group.currentText() == "UniprotId":
            print(self.proteins)
            proteins = self.file.toPlainText()
            uniprotid = self.loaded_protein.split(",")[0]
            print(uniprotid)
            self.proteins[uniprotid] = []
            if uniprotid != "all":
                for i in proteins.split("\n"):
                    print(i)
                    if i != "":
                        if i.startswith(">"):
                            begin = i.split()[5].strip()
                            end = i.split()[8].strip()
                        else:
                            self.proteins[uniprotid].append(Region(uniprotid, i.strip(), begin, end))
        self.update()

    def update_proteins(self):
        self.update_tab()
        all_regions = []
        all_proteins = []
        self.group = self.combo_group.currentText()
        self.combo.clear()
        for i in self.proteins.values():
            all_regions += list(i)

        if self.combo_group.currentText() == "UniprotId":
            all_proteins = []
            for region in self.proteins.items():
                if region[0] in self.lengths.keys():
                    all_proteins.append(
                        region[0] + ", regions:" + str(len(region[1])) + ", length " + str(self.lengths[region[0]]))
                else:
                    all_proteins.append(
                        region[0] + ", regions:" + str(len(region[1])) + ", length None")
            self.loaded_protein = ""
        elif self.combo_group.currentText() == "Species":
            for region in self.species.items():
                all_proteins.append(
                    region[0] + ", proteins:" + str(len(region[1])))
            self.loaded_protein = ""
        elif self.combo_group.currentText() == "Groups of Taxonomy (Cellular)":
            for region in self.kingdom.items():
                all_proteins.append(
                    region[0] + ", proteins:" + str(len(region[1])))
            self.loaded_protein = ""
        else:
            self.file.setText("")
        self.combo.addItems(
            ["all, proteins:" + str(len(self.proteins.keys())) + ", regions:" + str(
                len(all_regions))] + all_proteins)
        self.update()

    def update(self):
        self.fasta.proteins = self.proteins
        self.fasta.species = self.species
        self.fasta.cells = self.cells
        self.fasta.path = self.path
        self.fasta.lengths = self.lengths
        self.fasta.kingdom = self.kingdom

    def update_tab(self):
        self.proteins = self.fasta.proteins
        self.species = self.fasta.species
        self.cells = self.fasta.cells
        self.path = self.fasta.path
        self.lengths = self.fasta.lengths
        self.kingdom = self.fasta.kingdom
