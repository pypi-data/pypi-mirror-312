from PySide6.QtCharts import QChartView
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QWidget

from ..model.lenlab import Lenlab
from .vocabulary import Vocabulary as Vocab


class Oscilloscope(QWidget):
    title = Vocab("Oscilloscope", "Oszilloskop")

    def __init__(self, lenlab: Lenlab):
        super().__init__()

        self.lenlab = lenlab

        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        main_layout.addWidget(self.chart_view)

        sidebar_layout = QVBoxLayout()
        main_layout.addLayout(sidebar_layout)

        # start / stop
        layout = QHBoxLayout()
        sidebar_layout.addLayout(layout)

        button = QPushButton(str(Vocab.start))
        layout.addWidget(button)

        button = QPushButton(str(Vocab.stop))
        layout.addWidget(button)

        sidebar_layout.addStretch(1)
