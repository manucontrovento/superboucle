from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QSettings
from superboucle.preferences_ui import Ui_Dialog

   
class Preferences(QDialog, Ui_Dialog):
    
    COLOR_RED = "RED"
    COLOR_AMBER = "AMBER"
    
    MESSAGE_RESTART_SB = "Please restart Super Boucle to apply these changes."

    def __init__(self, parent):
        super(Preferences, self).__init__(parent)
        self.gui = parent
        self.setupUi(self)
        
        settings = QSettings('superboucle', 'session')
        # reading preferred grid size
        self.spinRows.setValue(int(settings.value('grid_rows', 8)))
        self.spinColumns.setValue(int(settings.value('grid_columns', 8)))
            
        # reading preferred recording color 
        if str(settings.value('rec_color', self.COLOR_AMBER)) == self.COLOR_RED:
#            self.rButtonAmberRecColor.checked = False
            self.rButtonRedRecColor.setChecked(True)     
        else:
#            self.rButtonRedRecColor.checked = False
            self.rButtonAmberRecColor.setChecked(True)
        
        self.cBoxShowScenesManager.setChecked(self.gui.show_scenes_on_start)
        self.cBoxShowScenesManager.stateChanged.connect(self.onCheckShowScenesOnStart)
        
        self.cBoxShowPlaylistManager.setChecked(self.gui.show_playlist_on_start)
        self.cBoxShowPlaylistManager.stateChanged.connect(self.onCheckShowPlaylistOnStart)       
        
        self.cBoxAutoconnect.setChecked(self.gui.auto_connect)
        self.cBoxAutoconnect.stateChanged.connect(self.onCheckAutoconnect)
        
#        self.cBoxPlaylistAccelerator.setChecked(self.gui.playlist_accelerators)
#        self.cBoxPlaylistAccelerator.stateChanged.connect(self.onCheckPlistAccelerators)
        
        self.cBoxShowDetailsWhenTriggered.setChecked(self.gui.show_clip_details_on_trigger)
        self.cBoxShowDetailsWhenTriggered.stateChanged.connect(self.onCheckShowClipDetails)   
        
        self.cBoxShowDetailsWhenVolumeChanged.setChecked(self.gui.show_clip_details_on_volume)
        self.cBoxShowDetailsWhenVolumeChanged.stateChanged.connect(self.onCheckShowClipDetailsWhenVolume)
        
        self.cBoxPlayAfterRecord.setChecked(self.gui.play_clip_after_record)
        self.cBoxPlayAfterRecord.stateChanged.connect(self.onCheckPlayClipAfterRecord) 
        
        self.rButtonAmberRecColor.toggled.connect(self.onAmberRecColor)
        self.rButtonRedRecColor.toggled.connect(self.onRedRecColor)
        
        self.labelMessage.setText("")
        
        self.setModal(True)
        self.show()

    def onAmberRecColor(self):
        self.labelMessage.setText(self.MESSAGE_RESTART_SB)
        
    def onRedRecColor(self):        
        self.labelMessage.setText(self.MESSAGE_RESTART_SB)
        
    def onCheckShowScenesOnStart(self):
        self.gui.show_scenes_on_start = self.cBoxShowScenesManager.isChecked()
    
    def onCheckShowPlaylistOnStart(self):
        self.gui.show_playlist_on_start = self.cBoxShowPlaylistManager.isChecked()
        
    def onCheckAutoconnect(self):
        self.gui.auto_connect = self.cBoxAutoconnect.isChecked()

#    def onCheckPlistAccelerators(self):
#       self.gui.playlist_accelerators = self.cBoxPlaylistAccelerator.isChecked()

    def onCheckShowClipDetails(self):
        self.gui.show_clip_details_on_trigger = self.cBoxShowDetailsWhenTriggered.isChecked()
        
    def onCheckShowClipDetailsWhenVolume(self):
        self.gui.show_clip_details_on_volume = self.cBoxShowDetailsWhenVolumeChanged.isChecked()
        
    def onCheckPlayClipAfterRecord(self):
        self.gui.play_clip_after_record = self.cBoxPlayAfterRecord.isChecked()        

    def closeEvent(self, event):
        settings = QSettings('superboucle', 'session')
        # saving preferred grid size
        settings.setValue('grid_columns', str(self.spinColumns.value()))   # Width
        settings.setValue('grid_rows', str(self.spinRows.value()))         # Heigh
        # saving recording color
        if self.rButtonRedRecColor.isChecked():
            settings.setValue('rec_color', self.COLOR_RED)
        else:
            settings.setValue('rec_color', self.COLOR_AMBER)
        
        #settings.sync()

    def onFinished(self):
        pass