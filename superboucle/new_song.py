from PyQt5.QtWidgets import QDialog
from superboucle.new_song_ui import Ui_Dialog
from superboucle.clip import Song
from PyQt5.QtCore import QSettings

class NewSongDialog(QDialog, Ui_Dialog):

    def __init__(self, parent):
        super(NewSongDialog, self).__init__(parent)
        self.gui = parent
        self.setupUi(self)
        
        # reading grid preferred size:
        settings = QSettings('superboucle', 'session')
        self.widthSpinBox.setValue(int(settings.value('grid_columns', 8)))
        self.heightSpinBox.setValue(int(settings.value('grid_rows', 8)))
        self.show()

    def accept(self):
        self.gui.initUI(Song(self.widthSpinBox.value(),
                             self.heightSpinBox.value()))
        super(NewSongDialog, self).accept()
