# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/manu/Applicazioni/SuperBoucle-Manu/superboucle/gui_ui.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 926)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("QMainWindow {background-color: black;}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setStyleSheet("#centralwidget {background-color: Black;}")
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_out = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_out.sizePolicy().hasHeightForWidth())
        self.frame_out.setSizePolicy(sizePolicy)
        self.frame_out.setMinimumSize(QtCore.QSize(236, 875))
        self.frame_out.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_out.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_out.setObjectName("frame_out")
        self.label_7 = QtWidgets.QLabel(self.frame_out)
        self.label_7.setGeometry(QtCore.QRect(0, 0, 131, 81))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setText("")
        self.label_7.setPixmap(QtGui.QPixmap(":/icons/icons/logo.png"))
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.frame_in = QtWidgets.QFrame(self.frame_out)
        self.frame_in.setGeometry(QtCore.QRect(0, 75, 236, 801))
        self.frame_in.setStyleSheet("#frame_in {\n"
"background-color: rgb(175, 178, 178);}")
        self.frame_in.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_in.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_in.setObjectName("frame_in")
        self.master_volume = QSuperDial(self.frame_in)
        self.master_volume.setGeometry(QtCore.QRect(170, 5, 60, 60))
        self.master_volume.setMaximumSize(QtCore.QSize(60, 60))
        self.master_volume.setStyleSheet("background-color: rgb(223, 27, 130);\n"
"color: black;")
        self.master_volume.setMaximum(256)
        self.master_volume.setObjectName("master_volume")
        self.label_6 = QtWidgets.QLabel(self.frame_in)
        self.label_6.setGeometry(QtCore.QRect(10, 10, 141, 31))
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color: rgb(160, 6, 89);")
        self.label_6.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.frame_clip = QtWidgets.QFrame(self.frame_in)
        self.frame_clip.setGeometry(QtCore.QRect(10, 280, 221, 511))
        self.frame_clip.setStyleSheet("#frame_clip {background-color: rgb(223, 223, 223);}")
        self.frame_clip.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_clip.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_clip.setObjectName("frame_clip")
        self.clip_name = QtWidgets.QLineEdit(self.frame_clip)
        self.clip_name.setGeometry(QtCore.QRect(0, 0, 221, 31))
        font = QtGui.QFont()
        font.setFamily("Noto Sans")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.clip_name.setFont(font)
        self.clip_name.setStyleSheet("#clip_name {background-color: black; color: rgb(255, 253, 24);}")
        self.clip_name.setAlignment(QtCore.Qt.AlignCenter)
        self.clip_name.setObjectName("clip_name")
        self.clip_description = QtWidgets.QLabel(self.frame_clip)
        self.clip_description.setGeometry(QtCore.QRect(5, 30, 211, 91))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.clip_description.setFont(font)
        self.clip_description.setToolTip("")
        self.clip_description.setToolTipDuration(5)
        self.clip_description.setStatusTip("")
        self.clip_description.setStyleSheet("color: white;\n"
"background-color: black;\n"
"border-radius: 2px;")
        self.clip_description.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.clip_description.setWordWrap(True)
        self.clip_description.setObjectName("clip_description")
        self.deleteButton = QtWidgets.QPushButton(self.frame_clip)
        self.deleteButton.setGeometry(QtCore.QRect(110, 480, 101, 23))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.deleteButton.setFont(font)
        self.deleteButton.setObjectName("deleteButton")
        self.exportButton = QtWidgets.QPushButton(self.frame_clip)
        self.exportButton.setGeometry(QtCore.QRect(110, 450, 101, 23))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.exportButton.setFont(font)
        self.exportButton.setObjectName("exportButton")
        self.normalizeButton = QtWidgets.QPushButton(self.frame_clip)
        self.normalizeButton.setGeometry(QtCore.QRect(10, 480, 91, 23))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.normalizeButton.setFont(font)
        self.normalizeButton.setObjectName("normalizeButton")
        self.revertButton = QtWidgets.QPushButton(self.frame_clip)
        self.revertButton.setGeometry(QtCore.QRect(10, 450, 91, 23))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.revertButton.setFont(font)
        self.revertButton.setObjectName("revertButton")
        self.groupBoxMuteGroup = QtWidgets.QGroupBox(self.frame_clip)
        self.groupBoxMuteGroup.setGeometry(QtCore.QRect(10, 290, 201, 31))
        font = QtGui.QFont()
        font.setFamily("Noto Sans")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.groupBoxMuteGroup.setFont(font)
        self.groupBoxMuteGroup.setObjectName("groupBoxMuteGroup")
        self.mute_group = QtWidgets.QSpinBox(self.groupBoxMuteGroup)
        self.mute_group.setGeometry(QtCore.QRect(130, 0, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.mute_group.setFont(font)
        self.mute_group.setObjectName("mute_group")
        self.groupBoxClipOffset = QtWidgets.QGroupBox(self.frame_clip)
        self.groupBoxClipOffset.setGeometry(QtCore.QRect(10, 160, 201, 91))
        font = QtGui.QFont()
        font.setFamily("Noto Sans")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.groupBoxClipOffset.setFont(font)
        self.groupBoxClipOffset.setObjectName("groupBoxClipOffset")
        self.formLayoutWidget_4 = QtWidgets.QWidget(self.groupBoxClipOffset)
        self.formLayoutWidget_4.setGeometry(QtCore.QRect(0, 20, 201, 62))
        self.formLayoutWidget_4.setObjectName("formLayoutWidget_4")
        self.formLayout_4 = QtWidgets.QFormLayout(self.formLayoutWidget_4)
        self.formLayout_4.setContentsMargins(0, 0, 0, 0)
        self.formLayout_4.setObjectName("formLayout_4")
        self.frame_offset = QtWidgets.QSpinBox(self.formLayoutWidget_4)
        self.frame_offset.setMinimum(-4410000)
        self.frame_offset.setMaximum(4410000)
        self.frame_offset.setObjectName("frame_offset")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.frame_offset)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget_4)
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(10)
        font.setItalic(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label = QtWidgets.QLabel(self.formLayoutWidget_4)
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(10)
        font.setItalic(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.label)
        self.beat_offset = QtWidgets.QDoubleSpinBox(self.formLayoutWidget_4)
        self.beat_offset.setEnabled(True)
        self.beat_offset.setMaximum(99.0)
        self.beat_offset.setSingleStep(0.01)
        self.beat_offset.setObjectName("beat_offset")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.beat_offset)
        self.groupBoxOutputPort = QtWidgets.QGroupBox(self.frame_clip)
        self.groupBoxOutputPort.setGeometry(QtCore.QRect(10, 240, 201, 51))
        font = QtGui.QFont()
        font.setFamily("Noto Sans")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.groupBoxOutputPort.setFont(font)
        self.groupBoxOutputPort.setObjectName("groupBoxOutputPort")
        self.output = QtWidgets.QComboBox(self.groupBoxOutputPort)
        self.output.setGeometry(QtCore.QRect(0, 20, 201, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.output.setFont(font)
        self.output.setObjectName("output")
        self.groupBoxBeat = QtWidgets.QGroupBox(self.frame_clip)
        self.groupBoxBeat.setGeometry(QtCore.QRect(10, 120, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.groupBoxBeat.setFont(font)
        self.groupBoxBeat.setObjectName("groupBoxBeat")
        self.beat_diviser = QtWidgets.QSpinBox(self.groupBoxBeat)
        self.beat_diviser.setGeometry(QtCore.QRect(130, 2, 71, 31))
        self.beat_diviser.setStyleSheet("")
        self.beat_diviser.setMinimum(1)
        self.beat_diviser.setMaximum(999)
        self.beat_diviser.setObjectName("beat_diviser")
        self.groupBoxClipVolume = QtWidgets.QGroupBox(self.frame_clip)
        self.groupBoxClipVolume.setGeometry(QtCore.QRect(10, 370, 201, 51))
        self.groupBoxClipVolume.setTitle("")
        self.groupBoxClipVolume.setObjectName("groupBoxClipVolume")
        self.labelClipVolume = QtWidgets.QLabel(self.groupBoxClipVolume)
        self.labelClipVolume.setGeometry(QtCore.QRect(0, 30, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelClipVolume.setFont(font)
        self.labelClipVolume.setStyleSheet("color: rgb(0, 170, 0);")
        self.labelClipVolume.setText("")
        self.labelClipVolume.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.labelClipVolume.setObjectName("labelClipVolume")
        self.clip_volume = QSuperDial(self.groupBoxClipVolume)
        self.clip_volume.setEnabled(True)
        self.clip_volume.setGeometry(QtCore.QRect(150, 0, 51, 51))
        self.clip_volume.setStyleSheet("background-color: rgb(0, 170, 0);\n"
"color: black;")
        self.clip_volume.setMaximum(256)
        self.clip_volume.setSingleStep(1)
        self.clip_volume.setObjectName("clip_volume")
        self.label_5 = QtWidgets.QLabel(self.groupBoxClipVolume)
        self.label_5.setGeometry(QtCore.QRect(0, 10, 141, 19))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: rgb(0, 170, 0);")
        self.label_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.one_shot_clip = QtWidgets.QCheckBox(self.frame_clip)
        self.one_shot_clip.setGeometry(QtCore.QRect(6, 330, 201, 29))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.one_shot_clip.setFont(font)
        self.one_shot_clip.setObjectName("one_shot_clip")
        self.playButton = QtWidgets.QPushButton(self.frame_in)
        self.playButton.setGeometry(QtCore.QRect(55, 140, 36, 30))
        self.playButton.setStyleSheet("QPushButton {background-color: rgb(0, 0, 0);}\n"
"QPushButton:pressed {background-color: rgb(98, 98, 98);}\n"
"")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/black_play_24.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.playButton.setIcon(icon1)
        self.playButton.setIconSize(QtCore.QSize(24, 24))
        self.playButton.setObjectName("playButton")
        self.pauseButton = QtWidgets.QPushButton(self.frame_in)
        self.pauseButton.setGeometry(QtCore.QRect(100, 140, 36, 30))
        self.pauseButton.setStyleSheet("QPushButton {background-color: rgb(0, 0, 0);}\n"
"QPushButton:pressed {background-color: rgb(98, 98, 98);}\n"
"")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons/black_pause_24.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pauseButton.setIcon(icon2)
        self.pauseButton.setIconSize(QtCore.QSize(24, 24))
        self.pauseButton.setObjectName("pauseButton")
        self.rewindButton = QtWidgets.QPushButton(self.frame_in)
        self.rewindButton.setGeometry(QtCore.QRect(10, 140, 36, 30))
        self.rewindButton.setStyleSheet("QPushButton {background-color: rgb(0, 0, 0);}\n"
"QPushButton:pressed {background-color: rgb(98, 98, 98);}\n"
"")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/icons/black_rewind_24.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rewindButton.setIcon(icon3)
        self.rewindButton.setIconSize(QtCore.QSize(24, 24))
        self.rewindButton.setObjectName("rewindButton")
        self.bbtLabel = QtWidgets.QLabel(self.frame_in)
        self.bbtLabel.setGeometry(QtCore.QRect(10, 70, 221, 61))
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.bbtLabel.setFont(font)
        self.bbtLabel.setStyleSheet("background-color: black;\n"
"color: rgb(0, 255, 0);")
        self.bbtLabel.setText("")
        self.bbtLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.bbtLabel.setObjectName("bbtLabel")
        self.gotoButton = QtWidgets.QPushButton(self.frame_in)
        self.gotoButton.setGeometry(QtCore.QRect(190, 140, 36, 30))
        self.gotoButton.setStyleSheet("QPushButton {background-color: rgb(0, 0, 0);}\n"
"QPushButton:pressed {background-color: rgb(98, 98, 98);}\n"
"")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/icons/black_goto_24.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.gotoButton.setIcon(icon4)
        self.gotoButton.setIconSize(QtCore.QSize(24, 24))
        self.gotoButton.setObjectName("gotoButton")
        self.recordButton = QtWidgets.QPushButton(self.frame_in)
        self.recordButton.setGeometry(QtCore.QRect(145, 140, 36, 30))
        self.recordButton.setStyleSheet("QPushButton {background-color: rgb(0, 0, 0);}\n"
"QPushButton:pressed {background-color: rgb(98, 98, 98);}\n"
"")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/icons/record_24.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.recordButton.setIcon(icon5)
        self.recordButton.setIconSize(QtCore.QSize(24, 24))
        self.recordButton.setObjectName("recordButton")
        self.labelMasterVolume = QtWidgets.QLabel(self.frame_in)
        self.labelMasterVolume.setGeometry(QtCore.QRect(10, 37, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelMasterVolume.setFont(font)
        self.labelMasterVolume.setStyleSheet("color: rgb(160, 6, 89);")
        self.labelMasterVolume.setText("")
        self.labelMasterVolume.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.labelMasterVolume.setObjectName("labelMasterVolume")
        self.labelRecording = QtWidgets.QLabel(self.frame_in)
        self.labelRecording.setGeometry(QtCore.QRect(192, 110, 41, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelRecording.setFont(font)
        self.labelRecording.setStyleSheet("color: rgb(255, 0, 0);")
        self.labelRecording.setObjectName("labelRecording")
        self.label_12 = QtWidgets.QLabel(self.frame_in)
        self.label_12.setGeometry(QtCore.QRect(14, 178, 119, 18))
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.label_12.setFont(font)
        self.label_12.setStyleSheet("color: rgb(160, 6, 89);")
        self.label_12.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_12.setObjectName("label_12")
        self.label_10 = QtWidgets.QLabel(self.frame_in)
        self.label_10.setGeometry(QtCore.QRect(14, 210, 38, 18))
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("color: rgb(160, 6, 89);")
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.bpm = QtWidgets.QDoubleSpinBox(self.frame_in)
        self.bpm.setGeometry(QtCore.QRect(136, 207, 91, 26))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bpm.sizePolicy().hasHeightForWidth())
        self.bpm.setSizePolicy(sizePolicy)
        self.bpm.setMinimum(1.0)
        self.bpm.setMaximum(260.0)
        self.bpm.setProperty("value", 120.0)
        self.bpm.setObjectName("bpm")
        self.label_11 = QtWidgets.QLabel(self.frame_in)
        self.label_11.setGeometry(QtCore.QRect(14, 242, 107, 18))
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.label_11.setFont(font)
        self.label_11.setStyleSheet("color: rgb(160, 6, 89);")
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.gotoTarget = QtWidgets.QSpinBox(self.frame_in)
        self.gotoTarget.setGeometry(QtCore.QRect(136, 174, 91, 26))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gotoTarget.sizePolicy().hasHeightForWidth())
        self.gotoTarget.setSizePolicy(sizePolicy)
        self.gotoTarget.setMinimum(1)
        self.gotoTarget.setMaximum(999999999)
        self.gotoTarget.setObjectName("gotoTarget")
        self.beat_per_bar = QtWidgets.QSpinBox(self.frame_in)
        self.beat_per_bar.setGeometry(QtCore.QRect(136, 239, 91, 26))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.beat_per_bar.sizePolicy().hasHeightForWidth())
        self.beat_per_bar.setSizePolicy(sizePolicy)
        self.beat_per_bar.setMinimum(1)
        self.beat_per_bar.setProperty("value", 4)
        self.beat_per_bar.setObjectName("beat_per_bar")
        self.labelVersion = QtWidgets.QLabel(self.frame_out)
        self.labelVersion.setGeometry(QtCore.QRect(150, -1, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelVersion.setFont(font)
        self.labelVersion.setStyleSheet("color: rgb(115, 115, 115);")
        self.labelVersion.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.labelVersion.setObjectName("labelVersion")
        self.verticalLayout.addWidget(self.frame_out)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.gridLayout_out = QtWidgets.QGridLayout()
        self.gridLayout_out.setContentsMargins(12, -1, -1, -1)
        self.gridLayout_out.setSpacing(0)
        self.gridLayout_out.setObjectName("gridLayout_out")
        spacerItem = QtWidgets.QSpacerItem(0, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_out.addItem(spacerItem, 0, 2, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_out.addLayout(self.gridLayout, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_out.addItem(spacerItem1, 2, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_out.addItem(spacerItem2, 1, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_out.addItem(spacerItem3, 3, 0, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_out.addItem(spacerItem4, 4, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout_out)
        self.horizontalLayout.setStretch(1, 9)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 400, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuDevice = QtWidgets.QMenu(self.menubar)
        self.menuDevice.setObjectName("menuDevice")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        MainWindow.setMenuBar(self.menubar)
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionSave_As = QtWidgets.QAction(MainWindow)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionAdd_Device = QtWidgets.QAction(MainWindow)
        self.actionAdd_Device.setObjectName("actionAdd_Device")
        self.actionFullScreen = QtWidgets.QAction(MainWindow)
        self.actionFullScreen.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        self.actionFullScreen.setObjectName("actionFullScreen")
        self.actionManage_Devices = QtWidgets.QAction(MainWindow)
        self.actionManage_Devices.setObjectName("actionManage_Devices")
        self.actionPlaylist_Editor = QtWidgets.QAction(MainWindow)
        self.actionPlaylist_Editor.setObjectName("actionPlaylist_Editor")
        self.actionPort_Manager = QtWidgets.QAction(MainWindow)
        self.actionPort_Manager.setObjectName("actionPort_Manager")
        self.actionScene_Manager = QtWidgets.QAction(MainWindow)
        self.actionScene_Manager.setObjectName("actionScene_Manager")
        self.actionPreferences = QtWidgets.QAction(MainWindow)
        self.actionPreferences.setObjectName("actionPreferences")
        self.actionLightDownDevice = QtWidgets.QAction(MainWindow)
        self.actionLightDownDevice.setObjectName("actionLightDownDevice")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addAction(self.actionQuit)
        self.menuDevice.addAction(self.actionAdd_Device)
        self.menuDevice.addAction(self.actionManage_Devices)
        self.menuDevice.addSeparator()
        self.menuView.addAction(self.actionFullScreen)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionScene_Manager)
        self.menuView.addAction(self.actionPlaylist_Editor)
        self.menuView.addAction(self.actionPort_Manager)
        self.menuView.addAction(self.actionPreferences)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuDevice.menuAction())
        self.menubar.addAction(self.menuView.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Super Boucle"))
        self.label_6.setText(_translate("MainWindow", "Master volume"))
        self.clip_description.setText(_translate("MainWindow", "Description"))
        self.deleteButton.setText(_translate("MainWindow", "Delete Clip"))
        self.exportButton.setText(_translate("MainWindow", "Export Sample"))
        self.normalizeButton.setText(_translate("MainWindow", "Normalize"))
        self.revertButton.setText(_translate("MainWindow", "Revert"))
        self.groupBoxMuteGroup.setTitle(_translate("MainWindow", "Mute group"))
        self.groupBoxClipOffset.setTitle(_translate("MainWindow", "Clip Offset"))
        self.label_2.setText(_translate("MainWindow", "Sample"))
        self.label.setText(_translate("MainWindow", "Beat"))
        self.groupBoxOutputPort.setTitle(_translate("MainWindow", "Output port"))
        self.groupBoxBeat.setTitle(_translate("MainWindow", "Beat amount"))
        self.label_5.setText(_translate("MainWindow", "Clip volume"))
        self.one_shot_clip.setText(_translate("MainWindow", "One-shot clip"))
        self.playButton.setToolTip(_translate("MainWindow", "Play"))
        self.pauseButton.setToolTip(_translate("MainWindow", "Pause"))
        self.rewindButton.setToolTip(_translate("MainWindow", "Rewind"))
        self.gotoButton.setToolTip(_translate("MainWindow", "Go to"))
        self.recordButton.setToolTip(_translate("MainWindow", "Pause"))
        self.labelRecording.setText(_translate("MainWindow", "REC"))
        self.label_12.setText(_translate("MainWindow", "Go to position"))
        self.label_10.setText(_translate("MainWindow", "BPM"))
        self.label_11.setText(_translate("MainWindow", "Beat per bar"))
        self.labelVersion.setText(_translate("MainWindow", "..."))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuDevice.setTitle(_translate("MainWindow", "Device"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.actionNew.setText(_translate("MainWindow", "New..."))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionOpen.setText(_translate("MainWindow", "Open..."))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionSave_As.setText(_translate("MainWindow", "Save As..."))
        self.actionSave_As.setShortcut(_translate("MainWindow", "Ctrl+Shift+S"))
        self.actionAdd_Device.setText(_translate("MainWindow", "Add Device..."))
        self.actionFullScreen.setText(_translate("MainWindow", "FullScreen"))
        self.actionFullScreen.setShortcut(_translate("MainWindow", "F11"))
        self.actionManage_Devices.setText(_translate("MainWindow", "Manage Devices..."))
        self.actionManage_Devices.setShortcut(_translate("MainWindow", "Ctrl+D"))
        self.actionPlaylist_Editor.setText(_translate("MainWindow", "Playlist Editor"))
        self.actionPlaylist_Editor.setShortcut(_translate("MainWindow", "Ctrl+P"))
        self.actionPort_Manager.setText(_translate("MainWindow", "Port Manager"))
        self.actionPort_Manager.setShortcut(_translate("MainWindow", "Ctrl+M"))
        self.actionScene_Manager.setText(_translate("MainWindow", "Scene Manager"))
        self.actionScene_Manager.setShortcut(_translate("MainWindow", "Ctrl+E"))
        self.actionPreferences.setText(_translate("MainWindow", "Preferences"))
        self.actionLightDownDevice.setText(_translate("MainWindow", "Light down device"))
from superboucle.qsuperdial import QSuperDial
import gui_rc
