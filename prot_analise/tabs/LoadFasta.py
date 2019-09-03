from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget, QTextEdit, QComboBox, QHBoxLayout, QGroupBox

from prot_analise.scripts.Region import Region


class LoadFasta(QWidget):
    def __init__(self, fasta):
        super().__init__()
        self.fasta = fasta
        self.go_grooup = ""
        self.path = ""
        self.proteins = {}
        self.lenths = {}
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

    def set_lenths(self, lenths):
        self.lenths = lenths
        self.update()

    def source_datas(self):
        self.path = self.nameEdit.toPlainText()
        print(self.path)

    def get_proteins(self):
        return list(self.proteins.keys())

    def get_path(self, path):
        self.update_tab()
        self.proteins = {}
        f = open(path, 'r')
        seq = 0
        for i in f.readlines():
            print(i)
            if i != "":
                if i.startswith(">s") and seq == 0:
                    seq = 1
                    seq_reg = ""
                    uniprotid = i.split("=")[2].split(";")[0]
                    print("1", uniprotid)
                    begin = i.split("=")[3].split(";")[0]
                    end = i.split("=")[4].split(";")[0]
                elif seq == 1 and i.startswith(">s"):
                    seq = 1
                    if uniprotid not in self.proteins.keys():
                        self.proteins[uniprotid] = [Region(uniprotid, seq_reg, begin, end)]
                    else:
                        if not self.get_region_by_seq(self.proteins[uniprotid], seq_reg, begin, end):
                            self.proteins[uniprotid].append(Region(uniprotid, seq_reg, begin, end))
                    seq_reg = ""
                    uniprotid = i.split("=")[2].split(";")[0]
                    begin = i.split("=")[3].split(";")[0]
                    end = i.split("=")[4].split(";")[0]
                elif seq == 1 and not i.startswith(">"):
                    seq_reg += i.strip()

        if uniprotid:
            if uniprotid not in self.proteins.keys():
                self.proteins[uniprotid] = [Region(uniprotid, seq_reg, begin, end)]
            else:
                if not self.get_region_by_seq(self.proteins[uniprotid], seq_reg, begin, end):
                    self.proteins[uniprotid].append(Region(uniprotid, seq_reg, begin, end))
        all_regions = []
        for i in self.proteins.values():
            all_regions += list(i)
        all_proteins = []
        for region in self.proteins.items():
            all_proteins.append(region[0] + ", regions:" + str(len(set(region[1]))))
        self.combo.setItems(
            ["all, proteins:" + str(len(self.proteins.keys())) + ", regions:" + str(len(all_regions))] + all_proteins)
        self.loaded_protein = ""
        self.update()

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
        text = ""
        self.file.setText(text)
        if self.combo_group.currentText() == "UniprotId":
            self.loaded_protein = str(self.combo.currentText()).split(",")[0]
            text = ""
            if self.loaded_protein != "all" and self.loaded_protein != "":
                for region in self.proteins[self.loaded_protein]:
                    text += ">protein = " + self.loaded_protein + " "
                    text += "begin = " + str(region.get_begin()) + " "
                    text += "end = " + str(region.get_end()) + " \n"
                    text += str(region.sequence) + "\n"

            self.file.setText(text)
        elif self.combo_group.currentText() == "Species":
            if not self.proteins:
                self.get_update()
            self.loaded_protein = str(self.combo.currentText()).split(",")[0]
            text = ""
            if self.loaded_protein != "all" and self.loaded_protein != "":
                for protein in self.species[self.loaded_protein]:
                    for region in self.proteins[protein]:
                        text += ">protein = " + protein + " "
                        text += "begin = " + str(region.get_begin()) + " "
                        text += "end = " + str(region.get_end()) + " \n"
                        text += str(region.sequence) + "\n"
        elif self.combo_group.currentText() == "Groups of Taxonomy (Cellular)":
            if not self.proteins:
                self.get_update()
            self.loaded_protein = str(self.combo.currentText()).split(",")[0]
            text = ""
            if self.loaded_protein != "all" and self.loaded_protein != "":
                for protein in self.kingdom[self.loaded_protein]:
                    for region in self.proteins[protein]:
                        text += ">protein = " + protein + " "
                        text += "begin = " + str(region.get_begin()) + " "
                        text += "end = " + str(region.get_end()) + " \n"
                        text += str(region.sequence) + "\n"
        self.file.setText(text)
        self.update()

    def get_region_by_seq(self, list, seq, begin, end):
        for sequence in list:
            if sequence.get_sequence() == seq and sequence.get_begin() == begin and sequence.get_end() == end:
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
        if self.combo_group.currentText() == "UniprotId":
            self.group = "UniprotId"
            self.combo.clear()
            all_regions = []
            for i in self.proteins.values():
                all_regions += list(i)
            all_proteins = []
            for region in self.proteins.items():
                all_proteins.append(region[0] + ", regions:" + str(len(region[1])))
            self.combo.addItems(
                ["all, proteins:" + str(len(self.proteins.keys())) + ", regions:" + str(
                    len(all_regions))] + all_proteins)
            all_regions = []
            for i in self.proteins.values():
                all_regions += list(i)
            all_proteins = []
            print(self.lenths)
            for region in self.proteins.items():
                if region[0] in self.lenths.keys():
                    all_proteins.append(
                        region[0] + ", regions:" + str(len(region[1])) + ", lenght " + str(self.lenths[region[0]]))
                else:
                    all_proteins.append(
                        region[0] + ", regions:" + str(len(region[1])) + ", lenght None")
            self.combo.addItems(
                ["all, proteins:" + str(len(self.proteins.keys())) + ", regions:" + str(
                    len(all_regions))] + all_proteins)
            self.loaded_protein = ""
        elif self.combo_group.currentText() == "Species":
            print(self.species)
            self.group = self.combo_group.currentText()
            self.combo.clear()
            all_regions = []
            for i in self.proteins.values():
                all_regions += list(i)
            all_proteins = []
            print(self.lenths)
            for region in self.species.items():
                all_proteins.append(
                    region[0] + ", proteins:" + str(len(region[1])))
            self.combo.addItems(
                ["all, proteins:" + str(len(self.proteins.keys())) + ", regions:" + str(
                    len(all_regions))] + all_proteins)
            self.loaded_protein = ""
        elif self.combo_group.currentText() == "Groups of Taxonomy (Cellular)":
            print(self.kingdom)
            self.group = self.combo_group.currentText()
            self.combo.clear()
            all_regions = []
            for i in self.proteins.values():
                all_regions += list(i)
            all_proteins = []
            print(self.lenths)
            for region in self.kingdom.items():
                all_proteins.append(
                    region[0] + ", proteins:" + str(len(region[1])))
            self.combo.addItems(
                ["all, proteins:" + str(len(self.proteins.keys())) + ", regions:" + str(
                    len(all_regions))] + all_proteins)
            self.loaded_protein = ""
        else:
            self.combo.clear()
            self.group = self.combo_group.currentText()
            self.file.setText("")
        self.update()

    def update(self):
        self.fasta.proteins = self.proteins
        self.fasta.species = self.species
        self.fasta.cells = self.cells
        self.fasta.path = self.path
        self.fasta.lenths = self.lenths
        self.fasta.kingdom = self.kingdom

    def update_tab(self):
        self.proteins = self.fasta.proteins
        self.species = self.fasta.species
        self.cells = self.fasta.cells
        self.path = self.fasta.path
        self.lenths = self.fasta.lenths
        self.kingdom = self.fasta.kingdom
