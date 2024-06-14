from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from ui import *
from ui.menu_btn.MenuButton import MenuButton

class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_widgets()

    def setup_widgets(self):
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)
        left_bar = QVBoxLayout()
        left_bar.setSpacing(0)
        left_bar.setContentsMargins(0,0,0,0)
        online_btn = MenuButton('Play online')
        offline_btn = MenuButton('Play offline')
        exit_btn = MenuButton('Exit')
        left_bar.addWidget(online_btn)
        left_bar.addWidget(offline_btn)
        left_bar.addWidget(exit_btn)
        left_bar.addStretch(1)
        layout.addLayout(left_bar, 3)

        background_img = QLabel()
        pixmap = QPixmap('resources/background.png')
        pixmap = pixmap.scaled(500, 500, Qt.AspectRatioMode.KeepAspectRatio)
        background_img.setPixmap(pixmap)
        background_img.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        background_img.setScaledContents(True)
        layout.addWidget(background_img, 6)
        # layout.addStretch(75)


        self.setLayout(layout)

        online_btn.pressed.connect(self._online_pressed)
        offline_btn.pressed.connect(self._offline_pressed)
        exit_btn.pressed.connect(self._exit_pressed)

    def _online_pressed(self):
        self.connect_dialog = LoadingDialog(self)
        self.connect_dialog.show()

        self.connect_coroutine = ConnectCoroutine()
        # connect_coroutine.setParent(self)
        self.connect_coroutine.done.connect(self._connect_finished)
        print('connected signal slot')
        self.connect_coroutine.start_()

    @Slot(bool, str)
    def _connect_finished(self, success, error_msg):
        print('finised')
        self.connect_dialog.accept()
        if success:
            from ui import OnlineMenu
            ScreenManager.instance.set_screen(OnlineMenu())
        else:
            print(f'Failed to connect to the server. Reason: {error_msg}')

    def _offline_pressed(self):
        from ui import OfflineMenu
        ScreenManager.instance.set_screen(OfflineMenu())

    def _exit_pressed(self):
        QApplication.exit(0)