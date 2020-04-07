# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/manu/Applicazioni/SuperBoucle-Manu/superboucle/add_clip_ui.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(398, 249)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 210, 381, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.emptyButton = QtWidgets.QRadioButton(Dialog)
        self.emptyButton.setGeometry(QtCore.QRect(40, 100, 99, 21))
        self.emptyButton.setObjectName("emptyButton")
        self.newButton = QtWidgets.QRadioButton(Dialog)
        self.newButton.setGeometry(QtCore.QRect(40, 20, 141, 21))
        self.newButton.setObjectName("newButton")
        self.useButton = QtWidgets.QRadioButton(Dialog)
        self.useButton.setGeometry(QtCore.QRect(40, 60, 81, 21))
        self.useButton.setObjectName("useButton")
        self.fileList = QtWidgets.QComboBox(Dialog)
        self.fileList.setGeometry(QtCore.QRect(140, 60, 251, 23))
        self.fileList.setObjectName("fileList")
        self.cBoxOneShotClip = QtWidgets.QCheckBox(Dialog)
        self.cBoxOneShotClip.setGeometry(QtCore.QRect(42, 150, 331, 41))
        self.cBoxOneShotClip.setObjectName("cBoxOneShotClip")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.emptyButton.setText(_translate("Dialog", "Empty clip"))
        self.newButton.setText(_translate("Dialog", "Load new file..."))
        self.useButton.setText(_translate("Dialog", "Use file"))
        self.cBoxOneShotClip.setText(_translate("Dialog", "One-shot clip"))
