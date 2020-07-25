from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QSettings
from superboucle.preferences import Preferences

from superboucle.mixerstrip_ui import Ui_Mixerstrip

import settings
import common



class Mixerstrip(QWidget, Ui_Mixerstrip):

    def __init__(self, parent, portname, index):
        super(Mixerstrip, self).__init__(parent)
        self.mixer = parent
        self.setupUi(self)
        self.strip_index = index

        # set port name
        self.port_name_label.setText(portname)
        self.port_name = portname

        # ...and PyQt object name:
        self.setObjectName(portname)


        # set mixer mode
        self.setMixerMode()

        # read mixer strip values
        self.readMixerstrip()


        # signals
        self.gain_knob.valueChanged.connect(self.writeGainValue)

        self.send1_knob.valueChanged.connect(self.writeSend1Value)
        self.send2_knob.valueChanged.connect(self.writeSend2Value)

        self.vol_slider.valueChanged.connect(self.writeVolumeValue)
        self.mute_checkbox.clicked.connect(self.writeMuteValue)

        self.to_master_checkbox.clicked.connect(self.writeToMasterValue)



    # set mixer mode
    def setMixerMode(self):
        if common.mixer_mode == False:
            self.drop_checkbox.hide()
            self.to_master_checkbox.hide()
        else:
            self.drop_checkbox.hide() # always hide until drops are implemented
            self.to_master_checkbox.show()



    # get and update each mixer values from mixer dict
    def readMixerstrip(self):
        # gain
        gain = settings.output_ports[self.port_name]["gain"]
        self.gain_knob.setValue(gain*200)
        self.gain_label.setText(str(round((gain*200 - 100))))

        # send1
        self.send1_knob.setValue(settings.output_ports[self.port_name]["send1"] * 100)
        # send2
        self.send2_knob.setValue(settings.output_ports[self.port_name]["send2"] * 100)

        # vol
        self.vol_slider.setValue(settings.output_ports[self.port_name]["vol"] * 100)
        # mute
        self.mute_checkbox.setChecked(settings.output_ports[self.port_name]["mute"])

        # to_master
        self.to_master_checkbox.setChecked(settings.output_ports[self.port_name]["to_master"])



    # Port name
    def getPortName(self):
        return self.port_name



    # write Gain into mixer dict
    def writeGainValue(self):
        gain = self.gain_knob.value()
        settings.output_ports[self.port_name]["gain"] = gain / 200
        self.gain_label.setText(str(round((gain-100))))

    # write Send1 into mixer dict
    def writeSend1Value(self):
        settings.output_ports[self.port_name]["send1"] = self.send1_knob.value() / 100

    # write Send2 into mixer dict
    def writeSend2Value(self):
        settings.output_ports[self.port_name]["send2"] = self.send2_knob.value() / 100

    # write Volume into mixer dict
    def writeVolumeValue(self):
        settings.output_ports[self.port_name]["vol"] = self.vol_slider.value() / 100
        
    # write Mute into mixer dict
    def writeMuteValue(self):
        settings.output_ports[self.port_name]["mute"] = bool(self.mute_checkbox.checkState())
        self.mixer.muteUpdated(self.port_name, self.strip_index)



    def writeToMasterValue(self):
        settings.output_ports[self.port_name]["to_master"] = bool(self.to_master_checkbox.checkState())
        #print(settings.output_ports)



    def updateGuiVolume(self):
        self.vol_slider.setValue(settings.output_ports[self.port_name]["vol"] * 100)

    def updateGuiSend1(self):
        self.send1_knob.setValue(settings.output_ports[self.port_name]["send1"] * 100)

    def updateGuiSend2(self):
        self.send2_knob.setValue(settings.output_ports[self.port_name]["send2"] * 100)

    def updateGuiMute(self):
        self.mute_checkbox.setChecked(settings.output_ports[self.port_name]["mute"])

