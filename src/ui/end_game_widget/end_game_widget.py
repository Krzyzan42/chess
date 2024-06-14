from PySide6.QtCore import *
from PySide6.QtWidgets import *

widget_style = '''
background-color: #333;
'''
class EndGameWidget(QWidget):
    pass
    # title_lbl :QLabel
    # reason_lbl :QLabel
    # white_name :QLabel
    # black_name :QLabel

    pass
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        layout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setFixedSize(300, 300)
        central_widget.setStyleSheet('background-color:black;')
        layout.addWidget(central_widget)
        self.setLayout(layout)


    # def setup_ui(self):
    #     root = QVBoxLayout() 

    #     self.title_lbl = QLabel()
    #     self.title_lbl.setText('Title')
    #     root.addWidget(self.title_lbl, alignment=Qt.AlignmentFlag.AlignHCenter)
    #     root.addWidget(QLabel())

    #     self.setLayout(root)

    # def animate(self, start_point :QPoint, end_point :QPoint):
    #     anim = QPropertyAnimation(self, b"pos")
    #     anim.setTargetObject(self)
    #     anim.setDuration(1000)
    #     anim.stateChanged.connect(lambda: print(self.size()))
    #     anim.setStartValue(start_point)
    #     anim.setEndValue(end_point)
    #     anim.start()
    #     self.anim = anim
        

    # def set_names(self, white :str, black :str, white_won :bool, reason :str):
    #     pass

    