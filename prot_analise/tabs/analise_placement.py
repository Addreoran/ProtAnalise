from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QFileDialog, QTextEdit, QGroupBox, QSlider
from PyQt5.QtWidgets import QVBoxLayout, QSizePolicy, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class AnalisePlacement(QWidget):
    def __init__(self, fasta):
        super().__init__()
        self.path = ""
        self.fasta = fasta
        self.lenths = {}
        self.popularity = []
        self.main_widget = QtWidgets.QWidget(self)
        self.proteins = self.fasta.proteins
        button3 = QtWidgets.QPushButton("Region placement plot")
        button3.clicked.connect(self.plot_placement)
        button4 = QtWidgets.QPushButton("Get region by placing")
        button4.clicked.connect(self.get_regions)

        self.layout2 = QVBoxLayout()

        checkGroup2 = QGroupBox("Get lenght of proteins from file.")
        layout3 = QHBoxLayout()

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(0)
        self.slider.setTickPosition(QSlider.TicksAbove)
        self.slider.setTickInterval(10)

        self.slider.valueChanged.connect(self.changedValue_min)
        self.sliderEdit = QTextEdit(self)
        self.sliderEdit.setMaximumHeight(30)
        self.sliderEdit.setMaximumWidth(60)
        self.slider2 = QSlider(Qt.Horizontal, self)
        self.slider2.setMinimum(1)
        self.slider2.setMaximum(101)
        self.slider2.setValue(20)
        self.slider2.setTickPosition(QSlider.TicksAbove)
        self.slider2.setTickInterval(10)
        self.slider2.setValue(100)
        self.slider2.valueChanged.connect(self.changedValue_max)
        self.slider2Edit = QTextEdit(self)
        self.slider2Edit.setMaximumHeight(30)
        self.slider2Edit.setMaximumWidth(60)
        layout3.addWidget(self.slider)
        layout3.addWidget(self.sliderEdit)
        layout3.addWidget(self.slider2)
        layout3.addWidget(self.slider2Edit)
        checkGroup2.setLayout(layout3)
        self.layout2.addWidget(button3)
        self.layout2.addWidget(checkGroup2)
        self.layout2.addWidget(button4)

        self.selctGroup2 = QGroupBox("")
        self.layout4 = QHBoxLayout()
        self.ended = QLabel("No lengths and taxonomic.")
        self.layout4.addWidget(self.ended)
        self.regions = QTextEdit(self)
        self.layout4.addWidget(self.regions)

        self.selctGroup2.setLayout(self.layout4)
        self.selctGroup2.hide()

        self.m = PlotCanvas()
        self.layout2.addWidget(self.selctGroup2)
        self.layout2.addWidget(self.m)
        self.setLayout(self.layout2)

    def changedValue_min(self):
        size = str(self.slider.value())
        self.sliderEdit.setText(size)

    def changedValue_max(self):
        size = str(self.slider2.value())
        self.slider2Edit.setText(size)

    def get_path(self):
        self.update_tab()
        filename = QFileDialog.getOpenFileName(self, "Open File", "./")
        if filename[0]:
            self.nameEdit.setText(filename[0])
        self.update()

    def plot_placement(self):
        self.update_tab()
        self.fasta.search_popularity()
        self.popularity = self.fasta.popularity
        names = list(range(0, 101))

        self.m.prepare_plot(names, [len(i) for i in self.popularity], self)

    def get_regions(self):
        self.update_tab()
        self.fasta.search_popularity()
        self.popularity = self.fasta.popularity
        try:
            min = int(self.sliderEdit.toPlainText())
        except:
            min = 0
        try:
            max = int(self.slider2Edit.toPlainText())
        except:
            max = 100
        if min > max:
            tmp_min = min
            min = max
            max = tmp_min
        text = ""
        for i in self.popularity[min:max]:
            for region in i:
                text += ">protein= " + region.uniprot_id + " "
                text += "begin= " + region.get_begin() + " "
                text += "end= " + region.get_end() + " \n"
                text += region.get_sequence() + "\n"
        self.regions.setText(text)
        self.selctGroup2.show()

    def update_tab(self):
        self.proteins = self.fasta.proteins
        self.species = self.fasta.species
        self.cells = self.fasta.cells
        self.path = self.fasta.path
        self.lenths = self.fasta.lenths
        self.kingdom = self.fasta.kingdom


class PlotCanvas(FigureCanvas):

    def __init__(self, names=None, popularity=None, width=5, height=4, dpi=100):
        if popularity is None:
            popularity = []
        if names is None:
            names = []
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.names = names
        self.popularity = popularity
        self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)

    def prepare_plot(self, names, popularity, parent):
        self.names = names
        self.popularity = popularity
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()

    def plot(self):
        ax = self.figure.add_subplot(111)
        ax.bar(self.names, self.popularity)
        ax.set_title('Distribution of regions in proteins')
        self.draw()
