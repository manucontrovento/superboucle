#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Gui
"""
from PyQt5.QtGui import QDesktopServices, QCloseEvent, QCursor
from PyQt5.QtWidgets import (QMainWindow, QFileDialog, QAction, QActionGroup, QMessageBox, QApplication)
from PyQt5.QtCore import QTimer, QObject, pyqtSignal, QSettings, Qt, QUrl
from superboucle.clip import Clip, load_song_from_file, verify_ext, Song
from superboucle.gui_ui import Ui_MainWindow
from superboucle.cell import Cell
from superboucle.learn import LearnDialog
from superboucle.device_manager import ManageDialog
from superboucle.playlist import PlaylistDialog
from superboucle.scene_manager import SceneManager
from superboucle.song_annotation import SongAnnotation
from superboucle.preferences import Preferences
from superboucle.about import About
from superboucle.assistant import Assistant
from superboucle.port_manager import PortManager

from superboucle.mixer import Mixer # <-------- MIXER WINDOW

from superboucle.new_song import NewSongDialog
from superboucle.add_clip import AddClipDialog
from superboucle.add_port import AddPortDialog
from superboucle.export_samples import ExportAllSamplesDialog
from superboucle.edit_clips import EditClipsDialog
from superboucle.device import Device
import struct
from queue import Queue, Empty
import pickle
from os.path import expanduser, dirname, isfile
import numpy as np
import soundfile as sf
import math
import time
import copy
import os
import settings
import common
import help

BAR_START_TICK = 0.0
BEATS_PER_BAR = 4.0
BEAT_TYPE = 4.0
TICKS_PER_BEAT = 960.0

EMPTY_SONG_NAME = "Empty Song"

class Gui(QMainWindow, Ui_MainWindow):
    NOTEON = 0x9
    NOTEOFF = 0x8
    MIDICTRL = 11

    GREEN = ("#cell_frame { border: 0px; border-radius: 10px; "
             "background-color: rgb(125,242,0);}")
    BLUE = ("#cell_frame { border: 0px; border-radius: 10px; "
            "background-color: rgb(0, 130, 240);}")
    RED = ("#cell_frame { border: 0px; border-radius: 10px; "
           "background-color: rgb(255, 21, 65);}")
    AMBER = ("#cell_frame { border: 0px; border-radius: 10px; "
             "background-color: rgb(255, 102, 0);}")
    PURPLE = ("#cell_frame { border: 0px; border-radius: 10px; "
              "background-color: rgb(130, 0, 240);}")
    DEFAULT = ("#cell_frame { border: 0px; border-radius: 10px; "
               "background-color: rgb(217, 217, 217);}")

    RECORD_BLINK = ("QPushButton {background-color: rgb(255, 255, 255);}"
                    "QPushButton:pressed {background-color: "
                    "rgb(98, 98, 98);}")

    RECORD_DEFAULT = ("QPushButton {background-color: rgb(0, 0, 0);}"
                      "QPushButton:pressed {background-color: "
                      "rgb(98, 98, 98);}")

    STATE_COLORS = {Clip.STOP: RED,
                    Clip.STARTING: GREEN,
                    Clip.START: GREEN,
                    Clip.STOPPING: RED,
                    Clip.PREPARE_RECORD: AMBER,
                    Clip.RECORDING: AMBER}
    STATE_BLINK = {Clip.STOP: False,
                   Clip.STARTING: True,
                   Clip.START: False,
                   Clip.STOPPING: True,
                   Clip.PREPARE_RECORD: True,
                   Clip.RECORDING: False}

    BLINK_DURATION = 200
    PROGRESS_PERIOD = 300

    updateUi = pyqtSignal()
    readQueueIn = pyqtSignal()
    updatePorts = pyqtSignal()
    songLoad = pyqtSignal()

    def __init__(self, song, jack_client, app):
        QObject.__init__(self)
        super(Gui, self).__init__()
        self._jack_client = jack_client
        self.app = app
        self.setupUi(self)
        self.clip_volume.knobRadius = 3
        self.is_learn_device_mode = False
        self.queue_out, self.queue_in = Queue(), Queue()
        self.updateUi.connect(self.update)
        self.readQueueIn.connect(self.readQueue)
        self.mixer_stripes_midi_linked = True # When false, moving faders and knobs and mutes on controller has no effect
        self.last_clip = None
        self.memory_clip = None
        self.songAnnotationDialog = None # Annotation window
        self.scenesManagerDialog = None
        self.current_scene = None
        self.shift_active = False
        self.output_mixer = None

        # Load devices
        self.deviceGroup = QActionGroup(self.menuDevice)
        self.devices = []

        if (settings.hasDevices == True and settings.devices):
            for raw_device in settings.devices:
                self.devices.append(Device(pickle.loads(raw_device)))
        else:
            self.devices.append(Device({'name': 'No Devices'}))            
            
        self.updateDevices()
        self.deviceGroup.triggered.connect(self.onDeviceSelect)

        ## Load song
        self.port_by_name = {}
        self.initUI(song)

        self.actionNew.triggered.connect(self.onActionNew)
        self.actionOpen.triggered.connect(self.onActionOpen)
        self.actionSave.triggered.connect(self.onActionSave)
        self.actionSave_As.triggered.connect(self.onActionSaveAs)
        self.actionQuit.triggered.connect(self.onActionQuit)

        self.actionAdd_Device.triggered.connect(self.onAddDevice)
        self.actionManage_Devices.triggered.connect(self.onManageDevice)
        self.actionRefresh.triggered.connect(self.onRefresh)

        self.actionPreferences.triggered.connect(self.onPreferences)
        self.actionPlaylist_Editor.triggered.connect(self.onPlaylistEditor)
        self.actionScene_Manager.triggered.connect(self.onSceneManager)

        self.actionExportAllSamples.triggered.connect(self.onExportAllClips)
        self.actionEditSelectedClips.triggered.connect(self.onEditSelectedClips)
        self.actionAutoAssignClipsColumn.triggered.connect(self.onAutoAssignClipsColumn)
        self.actionAutoAssignClipsOutput.triggered.connect(self.onAutoAssignClipsOutput)
        self.actionAutoAssignClipsSolo.triggered.connect(self.onAutoAssignClipsSolo)
        self.actionUnselectAllClips.triggered.connect(self.onUnselectAllClips)
        self.actionStopAllClips.triggered.connect(self.onStopAllClips)
        self.actionEditClipsOutputGroup.triggered.connect(self.onEditClipsByOutputPort)
        self.actionEditClipsMuteGroup.triggered.connect(self.onEditClipsByMuteGroup)

        self.actionPort_Manager.triggered.connect(self.onPortManager)
        self.actionMixer.triggered.connect(self.onMixer)

        self.actionFullScreen.triggered.connect(self.onActionFullScreen)
        self.actionAbout.triggered.connect(self.onActionAbout)
        self.actionOnline_Wiki.triggered.connect(self.onActionWiki)
        self.actionUserManual.triggered.connect(self.onActionUserManual)
        self.action_SongAnnotation.triggered.connect(self.onAction_SongAnnotation)

        self.song_volume_knob.valueChanged.connect(self.onSongVolumeChange)
        self.bpm.valueChanged.connect(self.onBpmChange)
        self.beat_per_bar.valueChanged.connect(self.onBeatPerBarChange)
        self.rewindButton.clicked.connect(self.onRewind)
        self.playButton.clicked.connect(self.onPlay)
        self.stopButton.clicked.connect(self.onStop)
        self.pauseButton.clicked.connect(self.onPause)
        self.gotoButton.clicked.connect(self.onGoto)
        self.recordButton.clicked.connect(self.onRecord)
        self.clip_name.textChanged.connect(self.onClipNameChange)
        self.clip_volume.valueChanged.connect(self.onClipVolumeChange)

        self.clip_info_combobox.currentTextChanged.connect(self.updateAllCellInfo)

        self.beat_diviser.valueChanged.connect(self.onBeatDiviserChange)
        self.output.activated.connect(self.onOutputChange)
        self.mute_group.valueChanged.connect(self.onMuteGroupChange)
        self.one_shot_clip.stateChanged.connect(self.onOneShotClip)
        self.lock_record.stateChanged.connect(self.onLockRecord)
        self.always_play_clip.stateChanged.connect(self.onAlwaysPlay)
        self.frame_offset.valueChanged.connect(self.onFrameOffsetChange)
        self.beat_offset.valueChanged.connect(self.onBeatOffsetChange)
        self.revertButton.clicked.connect(self.onRevertClip)
        self.normalizeButton.clicked.connect(self.onNormalizeClip)
        self.exportButton.clicked.connect(self.onExportClip)
        self.deleteButton.clicked.connect(self.onDeleteClipClicked)
        self.btnCopy.clicked.connect(self.onCopyDetailsClicked)
        self.btnPaste.clicked.connect(self.onPasteDetailsClicked)

        self.blktimer = QTimer()
        self.blktimer.state = False
        self.blktimer.timeout.connect(self.toggleBlinkButton)
        self.blktimer.start(self.BLINK_DURATION)

        self.disptimer = QTimer()
        self.disptimer.start(self.PROGRESS_PERIOD)
        self.disptimer.timeout.connect(self.updateProgress)

        self._jack_client.set_timebase_callback(self.timebase_callback)

        if settings.gui_geometry:
            self.restoreGeometry(settings.gui_geometry)

        # erase performance/system/cpu/whatever info:
        self.labelPerformanceInfo.setText("")
        
        # set tabClip to 1st tab:
        self.tabClip.setCurrentIndex(0)

        # reset clipping alert
        self.updateClipping(False)

        # set clip info combo box choices
        self.clip_info_combobox.clear()
        self.clip_info_combobox.addItems(["Volume",
                                          "File name",
                                          "Size in samples",
                                          "Size in beats",
                                          "Beat amount",
                                          "Port",
                                          "Solo clip group",
                                          "Sample offset",
                                          "Beat offset",
                                          "One-shot",
                                          "Lock record",
                                          "Always play"])



        self.show()

        # showing additional windows if desired:

        if settings.show_scenes_on_start == True:
            self.onSceneManager()

        if settings.show_playlist_on_start == True:
            self.onPlaylistEditor()

        self.activateWindow()
        self.setFocus()

    def initUI(self, new_song, loading = True):

        # remove old buttons
        self.btn_matrix = [[None for y in range(new_song.height)]
                           for x in range(new_song.width)]
        self.state_matrix = [[-1 for y in range(new_song.height)]
                             for x in range(new_song.width)]

        for i in reversed(range(self.gridLayout.count())):
            self.gridLayout.itemAt(i).widget().close()
            self.gridLayout.itemAt(i).widget().setParent(None)
              
        self.song = new_song

        if self.songAnnotationDialog:
             # Not a nice way but it's the only one I found:
            self.songAnnotationDialog.updateText(self.song.annotation)  

        # second pass with removing
        self.output.clear()
        self.output.addItems(common.toPortsList(settings.output_ports))
        self.song_volume_knob.setValue(int(common.toControllerVolumeValue(new_song.volume)))
        self.updateSongVolumeValue()
        self.bpm.setValue(new_song.bpm)
        self.beat_per_bar.setValue(new_song.beat_per_bar)
        for x in range(new_song.width):
            for y in range(new_song.height):
                clip = new_song.clips_matrix[x][y]
                cell = Cell(self, clip, x, y)
                self.btn_matrix[x][y] = cell
                self.gridLayout.addWidget(cell, y, x)

        if loading == True:

            # send device init command
            for init_cmd in self.device.init_command:
                self.queue_out.put(init_cmd)
    
            self.setWindowTitle(self.getWindowTitle(new_song.file_name or EMPTY_SONG_NAME))
            self.labelRecording.setVisible(False)
            self.labelShift.setVisible(False)

            if self.song.initial_scene in self.song.scenes:
                self.song.loadScene(self.song.initial_scene)

                # Lighting up initial scenes button:
                self.updateScenesButtons(self.song.initial_scene)
        
        self.update()
        
        if self.device:
            time.sleep(0.5) # wait for all init and light signals to be processed by controller
            
        self.songLoad.emit()


    # updating clipping alert

    def updateClipping(self, clipping=False):
        if clipping == False:
            stylesheet = 'color: none;'
        else:
            stylesheet = 'color: red;'

        self.clipping_label.setStyleSheet(stylesheet)


    # help management --------------------------------------------------------

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_H:  # if pressed key is H (help)

            pos = QCursor.pos()
            widget = QApplication.widgetAt(pos)   # this is widget under cursor

            if widget is None: return
            accName = widget.accessibleName()     # this is widget accessible name
            
            if accName != "":
                wantedHelp = help.Context(accName)  # Conversion of string accessible name to Context enum
                self.showContextHelp(wantedHelp)
                

    def showContextHelp(self, wantedHelp):
        helpText = help.getContextHelp(wantedHelp)
        Assistant(self, helpText, Assistant.MODE_CONTEXT)
    
    def onActionUserManual(self):
        helpText = help.getUserManual(help.ManualSection.Manual_All)
        Assistant(self, helpText, Assistant.MODE_MANUAL)

    # --------------------------------------------------------------------------------

    def openSongFromDisk(self, file_name):
        self._jack_client.transport_stop()
        self._jack_client.transport_locate(0)

        message = QMessageBox(self)
        message.setWindowTitle("Loading")
        message.setText("Reading files, please wait...")
        message.setModal(False)
        message.update()
        message.show()
        self.initUI(load_song_from_file(file_name))
        message.close()
        message = None

        self.redraw()
              
        # load annotations
        if settings.show_song_annotation_on_load:
            if self.songAnnotationDialog:
                self.songAnnotationDialog.close()
                self.songAnnotationDialog.destroy()

            self.showSongAnnotation()


    def showSongAnnotation(self):
        self.songAnnotationDialog = SongAnnotation(self)
        self.action_SongAnnotation.setEnabled(False)

    def moveEvent(self, event):
        settings.gui_geometry = self.saveGeometry()


    def closeEvent(self, event):
        response = QMessageBox.question(self, "Quit SpinTool", "Are you sure you want to quit SpinTool?")
        if response == QMessageBox.No:
            event.ignore()
        else:
            event.accept()
            self.onApplicationExit()
    

    def onApplicationExit(self):
        settings.gui_geometry = self.saveGeometry()
        
        #device lights turn off, if exhisting. Prevents device from remaining lighted-up
        try:
            # send init command
            self.onDeviceSelect()

            self.lightDownDevice()
            print("device light off")

        except:
            print("no device connected")  # Could not turn off device lights
        time.sleep(1)
        # Sorry for this bad coding. But I tried in all other ways, if you don't wait a while to let
        # the engine process pending midi messages, the device doesn't light off.
       
        settings.devices = [pickle.dumps(x.mapping)
                            for x in self.devices]



        # reset mixer settings if wanted
        if settings.save_mixerstrip_gain == False:
            common.resetGain(settings.output_ports)

        if settings.save_mixerstrip_send1 == False:
            common.resetSend1(settings.output_ports)

        if settings.save_mixerstrip_send2 == False:
            common.resetSend2(settings.output_ports)

        if settings.save_mixerstrip_volume == False:
            common.resetVolume(settings.output_ports)

        if settings.save_mixerstrip_mute == False:
            common.resetMute(settings.output_ports)

        print("Updating settings")
        settings.update()
        print("Settings updated")


    def onStartStopClicked(self):
        clip = self.sender().parent().parent().clip
        self.startStop(clip.x, clip.y)


    def startStop(self, x, y, controller = False):
        clip = self.btn_matrix[x][y].clip # affected clip
        
        if clip is None:
            if controller == False:
                # No clip instanced
                return
            
            elif controller == True and self.song.is_record:
                # Clip is none, but triggering came from controller

                if settings.allow_record_empty_clip == False:
                    # if recording on a empty clip is not allowed:
                    print("Recording on empty clip is not allowed") 
                    return
                
                else:
                    if (x + 1) > self.song.width or (y + 1) > self.song.height:
                        print("Required coordinates exceed grid dimension")
                        return 

                    # else a new clip and a new cell are instanced:
                    # print("Instancing a Clip: x = " + str(x) + ", y = " + str(y))

                    clip = Clip(audio_file=None, name='audio-%02d' % len(self.song.clips))
                    clip.x = x
                    clip.y = y
                    clip.one_shot = False
                    clip.lock_rec = False
                    clip.always_play = False
                    clip.beat_diviser = self.song.beat_per_bar

                    cell = Cell(self, clip, x, y)
                    self.btn_matrix[x][y] = cell
                    self.gridLayout.addWidget(cell, y, x)

                    cell.setClip(clip, False)
                    
                    if settings.auto_assign_new_clip_column:
                        self.autoAssignClipColumn(clip)


                    self.updateClipInfo()


        if self.song.is_record:
            # If clip is not None and clip.lock_rec == True

            if clip.lock_rec == True:
                print("This clip is LOCKED for recording")
                
            else:
                self.song.is_record = False
                self.updateRecordControls()
                # calculate buffer size
                state, position = self._jack_client.transport_query()
                bps = position['beats_per_minute'] / 60
                fps = position['frame_rate']
                size = int((1 / bps) * clip.beat_diviser * fps)
                self.song.init_record_buffer(clip, 2, size, fps)
                # set frame offset based on jack block size
                clip.frame_offset = self._jack_client.blocksize
                clip.state = Clip.PREPARE_RECORD
                self.recordButton.setStyleSheet(self.RECORD_DEFAULT)
        else:
            self.song.toggle(clip.x, clip.y)
            
            # to automatically view clip details, when triggered:
            if settings.show_clip_details_on_trigger:
                self.last_clip = clip
                self.updateClipInfo()
            

        self.update()



    def getClipInfo(self, clip):
        state, position = self._jack_client.transport_query()
        fps = position['frame_rate']
        bps = self.bpm.value() / 60
        size_in_frames = self.song.length(clip)
        if self.bpm.value() and fps:
            size_in_beats = (bps / fps) * size_in_frames
        else:
            size_in_beats = 0
        audio_file_name = clip.audio_file

        return size_in_frames, size_in_beats, audio_file_name



    def updateClipInfo(self, updateDetailsOnly = False):
        if self.last_clip:
            self.groupBoxClip.setEnabled(True)
            self.clip_name.setText(self.last_clip.name)
            self.frame_offset.setValue(self.last_clip.frame_offset)
            self.beat_offset.setValue(self.last_clip.beat_offset)
            self.beat_diviser.setValue(self.last_clip.beat_diviser)
            self.output.setCurrentText(self.last_clip.output)
            self.mute_group.setValue(self.last_clip.mute_group)
            self.clip_volume.setValue(common.toControllerVolumeValue(self.last_clip.volume))
            self.updateClipParameterChange()
            self.one_shot_clip.setChecked(self.last_clip.one_shot)
            self.lock_record.setChecked(self.last_clip.lock_rec)
            self.always_play_clip.setChecked(self.last_clip.always_play)
            
            if (updateDetailsOnly == False):

                # get clip info
                size_in_frames, size_in_beats, audio_file_name = self.getClipInfo(self.last_clip)

                clip_description = ("Size in samples: %s\nSize in beats: %s\nFile name: %s"
                                    % (size_in_frames, round(size_in_beats, 2), audio_file_name))

                self.clip_description.setText(clip_description)


            # update cell info
            self.updateAllCellInfo()



    # show clip details on edit button click - for button design only
    def onEdit(self):
        self.last_clip = self.sender().parent().parent().clip
        self.updateClipInfo()


    # show clip details on right click
    def onEditRightClick(self, clip):
        self.last_clip = clip
        self.updateClipInfo()


    # add clip on empty cell from add button and from cell frame
    def onAddClipOnEmptyCell(self, cell):
        if QApplication.keyboardModifiers() == Qt.ControlModifier:
            cell.setClip(cell.openClip())
        else:
            AddClipDialog(self, cell)

        self.updateClipInfo()


    def onRevertClip(self):
        if self.last_clip and self.last_clip.audio_file:
            audio_file = self.last_clip.audio_file
            self.song.data[audio_file] = self.song.data[audio_file][::-1]

    def onStopAllClips(self):
        self.song.stopAllClips()
        self.update()


    def onUnselectAllClips(self):
        for x in range(self.song.width):
            for y in range(self.song.height):
                cell = self.btn_matrix[x][y]
                cell.clipSelect(False)


    def onEditSelectedClips(self):
        self.EditClips(common.CLIPS_EDIT_MODE_ALL_SELECTED)

    def onEditClipsByMuteGroup(self):
        self.EditClips(common.CLIPS_EDIT_MODE_BY_MUTE_GROUP)

    def onEditClipsByOutputPort(self):
        self.EditClips(common.CLIPS_EDIT_MODE_BY_OUTPUT_PORT)

    def onAutoAssignClipsColumn(self):
        response = QMessageBox.question(self, "Automatic Output Port and Solo Group assignment", 
                                        "The same Output Port will be assigned to all clips in a column, " +
                                        "from first column on the left to last one the right, following the " +
                                        "same order of Output ports (stripes) in Mixer. \n\n" +
                                        "Clips Solo groups will be assigned too, numbered from 1 to " + str(self.song.width) + 
                                        " so that each clip will mute all the others of the same column, when triggered. \n\n " + 
                                        "SELECTED clips (Shift + Left click) will be excluded. If you want to exclude some clips " + 
                                        "from auto-assignment, you can select them. \n\n" +
                                        "Do you want to proceed?")
        if response == QMessageBox.No:
            return
        
        for nclip in self.song.clips:
            self.autoAssignClipColumn(nclip, True, True)

    def onAutoAssignClipsOutput(self):
        response = QMessageBox.question(self, "Automatic Output Port assignment", 
                                        "The same Output Port will be assigned to all clips in a column, " +
                                        "from first column on the left to last one the right, following the " +
                                        "same order of Output ports (stripes) in Mixer. \n\n" +
                                        "SELECTED clips (Shift + Left click) will be excluded. If you want to exclude some clips " + 
                                        "from auto-assignment, you can select them. \n\n" +                                        
                                        "Do you want to proceed?")
        if response == QMessageBox.No:
            return
        
        for nclip in self.song.clips:
            self.autoAssignClipColumn(nclip, True, False)

    def onAutoAssignClipsSolo(self):
        response = QMessageBox.question(self, "Automatic Solo Group assignment", 
                                        "The same Solo Group will be assigned to all clips in a column, " + 
                                        "numbered from 1 to " + str(self.song.width) + " so that each clip" +
                                        "  will mute all the others of the same column, when triggered. \n\n " + 
                                        "SELECTED clips (Shift + Left click) will be excluded. If you want to exclude some clips " + 
                                        "from auto-assignment, you can select them. \n\n" +                                        
                                        "Do you want to proceed?")
        if response == QMessageBox.No:
            return
        
        for nclip in self.song.clips:
            self.autoAssignClipColumn(nclip, False, True)            

    def autoAssignClipColumn(self, nclip, output=True, solo=True):
        if nclip.selected == True:
            return

        if solo == True:    
            nclip.mute_group = (nclip.x + 1)

        if output == True:
            out_port = common.getOutputPortByIndex(settings.output_ports, (nclip.x))
            if out_port:
                nclip.output = out_port
            else:
                nclip.output = common.DEFAULT_PORT

        if nclip is self.last_clip:
            self.updateClipInfo()
        
        return

    def EditClips(self, edit_mode):
        selected_clips = []

        clip_list = ""

        if edit_mode == common.CLIPS_EDIT_MODE_ALL_SELECTED:

            for x in range(self.song.width):
                for y in range(self.song.height):
                    clip = self.song.clips_matrix[x][y]
                    if clip and clip.selected == True:
                        selected_clips.append(clip)
                        clip_list += (clip.name + "\n")
            
            if selected_clips.__len__() == 0:
                message = QMessageBox(self)
                message.setWindowTitle("No clips selected")
                message.setText("Couldn't find any selected clip.\nHold SHIFT on PC keyboard and left-click any clip on the grid to select it")
                message.show()
                return

        editClipsDialog = EditClipsDialog(self, edit_mode, selected_clips)
        editClipsDialog.exec_()

        if editClipsDialog.proceed == False:
            editClipsDialog = None
            return

        if edit_mode == common.CLIPS_EDIT_MODE_BY_MUTE_GROUP and editClipsDialog.getMuteGroup() != 0:
            for nclip in self.song.clips:
                if nclip.mute_group == editClipsDialog.getMuteGroup():
                    selected_clips.append(nclip)
                    clip_list += (nclip.name + "\n")

        elif edit_mode == common.CLIPS_EDIT_MODE_BY_OUTPUT_PORT and editClipsDialog.getOutputPort() != "":
            for nclip in self.song.clips:
                if nclip.output == editClipsDialog.getOutputPort():
                    selected_clips.append(nclip)
                    clip_list += (nclip.name + "\n")                    

        if selected_clips.__len__() == 0:
            message = QMessageBox(self)
            message.setWindowTitle("No clips found")
            message.setText("Couldn't find any clip matching the selection")
            message.show()
            return

        clip_volume, change_mode = editClipsDialog.getVolumeAmount()
        analogVolume = common.toAnalogClipVolumeValue(clip_volume)

        clips_count = 0

        for nclip in selected_clips:

            if editClipsDialog.getEditMuteGroup() == True:
                nclip.mute_group = editClipsDialog.getMuteGroup()

            if editClipsDialog.getEditOutputPort() == True:
                nclip.output = editClipsDialog.getOutputPort()

            if editClipsDialog.getEditVolume() == True:

                if change_mode == common.SET_VOLUME:
                    nclip.volume = analogVolume

                elif change_mode == common.INCREASE_VOLUME:
                    new_volume = nclip.volume + analogVolume
                    if new_volume > 1:
                        new_volume = 1
                    nclip.volume = new_volume
                    
                elif change_mode == common.DECREASE_VOLUME:
                    new_volume = nclip.volume - analogVolume
                    if new_volume < 0:
                        new_volume = 0
                    nclip.volume = new_volume

            if nclip is self.last_clip:
                self.updateClipInfo()

            clips_count += 1

        if (editClipsDialog.getEditMuteGroup() == True or 
            editClipsDialog.getEditOutputPort() == True or
            editClipsDialog.getEditVolume() == True):

            message = QMessageBox(self)
            message.setWindowTitle(str(clips_count) + " clips processed")
            message.setText("The following clips have been processed: \n\n" + clip_list)
            message.show()

        if edit_mode == common.CLIPS_EDIT_MODE_ALL_SELECTED and editClipsDialog.getUnselectClips() == True:
            self.onUnselectAllClips()

        editClipsDialog = None
        self.update()
        
    def onExportAllClips(self):

        if self.song.clips.__len__() == 0:
            message = QMessageBox(self)
            message.setWindowTitle("Nothing to export")
            message.setText("Couldn't find any clip to export in current song")
            message.show()
            return

        if self._jack_client.transport_state == 1: # ROLLING

            response = QMessageBox.question(self, "Export all samples?", "Are you sure to export all samples? The song execution will be stopped")
            if response == QMessageBox.No:
                return
            
            self._jack_client.transport_stop()
            self._jack_client.transport_locate(0)

        suggestedPath = settings.paths_used.get(common.SONG_FILE_TYPE, expanduser('~'))
        exportDialog = ExportAllSamplesDialog(self)
        exportDialog.setPath(suggestedPath)
        exportDialog.exec_()
      
        selectedPath = exportDialog.getPath()
        normalize = exportDialog.getNormalize()
        prefixX = exportDialog.getX()
        prefixY = exportDialog.getY()
        proceed = exportDialog.proceed

        exportDialog = None

        if proceed == True:
            
            if os.path.isdir(selectedPath) == False:

                message = QMessageBox(self)
                message.setWindowTitle("Invalid directory path")
                message.setText("No exporting path selected, or invalid path")
                message.show()
                return
                
            message = QMessageBox(self)
            message.setWindowTitle("Exporting..")
            message.setText("Exporting clip samples, please wait")
            message.show()

            clips_count = 0

            for x in range(self.song.width):
                for y in range(self.song.height):
                    
                    clip = self.song.clips_matrix[x][y]

                    if clip and clip.audio_file:

                        clips_count += 1
                        audio_file = clip.audio_file
                        sample_rate = self.song.samplerate[clip.audio_file]
                        export_data = copy.deepcopy(self.song.data[audio_file])
                        
                        if normalize:
                            message.setText("Normalizing " + clip.name)
                            absolute_val = np.absolute(export_data)
                            current_level = np.ndarray.max(absolute_val)
                            export_data[:] *= (1 / current_level)

                        clip_position_name = prefixX + str(x) + '_' + prefixY + str(y) + '_' + clip.name + '.wav'

                        file_name = os.path.join(selectedPath, clip_position_name)
                        file_name = verify_ext(file_name, 'wav')

                        message.setText("Writing " + clip.name)

                        sf.write(file_name, export_data, sample_rate, subtype=sf.default_subtype('WAV'), format='WAV')

            if (clips_count == 0):
                message.setText("Couldn't find any sample to export in current song")
            else:
                message.close()

            message = None
            

    def onNormalizeClip(self):
        if self.last_clip and self.last_clip.audio_file:
            audio_file = self.last_clip.audio_file
            absolute_val = np.absolute(self.song.data[audio_file])
            current_level = np.ndarray.max(absolute_val)
            self.song.data[audio_file][:] *= (1 / current_level)


    def onExportClip(self):
        if self.last_clip and self.last_clip.audio_file:
            audio_file = self.last_clip.audio_file
            file_name, a = self.getSaveFileName('Clip : %s' % self.last_clip.name, 'WAVE (*.wav)')

            if file_name:
                file_name = verify_ext(file_name, 'wav')
                sf.write(file_name, self.song.data[audio_file],
                         self.song.samplerate[audio_file],
                         subtype=sf.default_subtype('WAV'),
                         format='WAV')


    def onDeleteClipClicked(self):
        if self.last_clip:
            response = QMessageBox.question(self, "Delete Clip?", ("Are you sure to delete the clip?"))
            if response == QMessageBox.Yes:
                self.song.removeClip(self.last_clip)
                self.initUI(self.song, False)



    # song vol update
    def updateSongVolumeValue(self):
        self.labelMasterVolume.setText(str(common.toDigitalVolumeValue(self.song.volume)*2))  # showing volume numeric value
        if self.output_mixer:
            self.output_mixer.updateSongVolumeGui(common.toControllerVolumeValue(self.song.volume)) # = * 256


    # song vol
    def onSongVolumeChange(self):
        self.song.volume = common.toAnalogVolumeValue(self.song_volume_knob.value()) # = / 256
        self.updateSongVolumeValue()



    def onBpmChange(self):
        self.song.bpm = self.bpm.value()

    def onBeatPerBarChange(self):
        self.song.beat_per_bar = self.beat_per_bar.value()

    def onGoto(self):

        state, position = self._jack_client.transport_query()
        new_position = (position['beats_per_bar']
                        * (self.gotoTarget.value() - 1)
                        * position['frame_rate']
                        * (60 / position['beats_per_minute']))
        self._jack_client.transport_locate(int(round(new_position, 0)))


    def onStop(self):
                
        self._jack_client.transport_stop()
        self.onRewind()
        self.updateMidiStop()

        if settings.prevent_song_save:
            # enabling song save
            self.songSavingEnabled(True)


    def onPause(self):
                
        self._jack_client.transport_stop()
        self.updateMidiPause()
        # update matrix and midi device
        self.redraw()

        if settings.prevent_song_save:
            # enabling song save
            self.songSavingEnabled(True)


    def onPlay(self):
                
        self._jack_client.transport_start()
        self.updateMidiPlay()
        # update matrix and midi device
        self.redraw()

        if settings.prevent_song_save:
            # disabling song save
            self.songSavingEnabled(False)


    def onRewind(self):

        self._jack_client.transport_locate(0)

        # reset progress bars
        self.resetAllClipProgressBars()

        # update matrix and midi device
        self.redraw()


    def onRecord(self):
                
        self.song.is_record = not self.song.is_record
        self.updateRecordControls()
    

    def onShift(self):
        self.shift_active = not self.shift_active
        self.updateShiftActive()


    def songSavingEnabled(self, enabled):
        # needs to be written with if/else;
        # because passing enabled as argument somehow doesn't work
        if enabled == True:
            self.actionSave.setEnabled(True)
            self.actionSave_As.setEnabled(True)
        else:
            self.actionSave.setEnabled(False)
            self.actionSave_As.setEnabled(False)



    def updateRecordControls(self):
        self.labelRecording.setVisible(self.song.is_record)
        
        if not self.song.is_record:
            self.recordButton.setStyleSheet(self.RECORD_DEFAULT)

        if self.device.record_btn:
            (msg_type, channel, pitch, velocity) = self.device.record_btn
            if self.song.is_record:
                if settings.rec_color == settings.COLOR_AMBER:
                    color = self.device.blink_amber_vel
                else:
                    color = self.device.blink_red_vel
            else:
                color = self.device.black_vel
            self.queue_out.put(((msg_type << 4) + channel, pitch, color))
    

    def updateShiftActive(self):
        self.labelShift.setVisible(self.shift_active)

        if self.shift_active == True:
            color = self.device.green_vel
        else:
            color = self.device.black_vel

        (a, b_channel, b_pitch, b) = self.device.shift_btn
        note = ((a << 4) + b_channel, b_pitch, color)
        self.queue_out.put(note)




    # update specific cell with clip parameter info
    def updateCellInfo(self, cell, clip):

        cell.labelVolume.setStyleSheet('font: bold 12pt "Noto Sans";')

        if self.clip_info_combobox.currentText() == "Volume":
            cell.labelVolume.setText(str(common.toDigitalVolumeValue(clip.volume)))

        if self.clip_info_combobox.currentText() == "Beat amount":
            cell.labelVolume.setText(str(clip.beat_diviser))

        if self.clip_info_combobox.currentText() == "Sample offset":
            cell.labelVolume.setText(str(clip.frame_offset))

        if self.clip_info_combobox.currentText() == "Beat offset":
            cell.labelVolume.setText(str(clip.beat_offset))

        if self.clip_info_combobox.currentText() == "Port":
            cell.labelVolume.setText(str(clip.output))

        if self.clip_info_combobox.currentText() == "Solo clip group":
            cell.labelVolume.setText(str(clip.mute_group))

        if self.clip_info_combobox.currentText() == "One-shot":
            cell.labelVolume.setText(str(clip.one_shot))

        if self.clip_info_combobox.currentText() == "Lock record":
            cell.labelVolume.setText(str(clip.lock_rec))

        if self.clip_info_combobox.currentText() == "Always play":
            cell.labelVolume.setText(str(clip.always_play))

        size_in_frames, size_in_beats, audio_file_name = self.getClipInfo(clip) # better: save this info into clip

        if self.clip_info_combobox.currentText() == "Size in samples":
            cell.labelVolume.setText(str(size_in_frames))

        if self.clip_info_combobox.currentText() == "Size in beats":
            cell.labelVolume.setText(str(round(size_in_beats, 2)))

        if self.clip_info_combobox.currentText() == "File name":
            cell.labelVolume.setText(audio_file_name)
            cell.labelVolume.setStyleSheet('font: 8pt "Noto Sans";')



    # update parameter info of all cells
    def updateAllCellInfo(self):
        for i in self.btn_matrix:
            for j in i:
                #print(j.pos_x, j.pos_y)
                if j.clip:
                    #print(j.clip.name)
                    cell = self.btn_matrix[j.pos_x][j.pos_y]
                    self.updateCellInfo(cell, j.clip)




    # reset all clip progress bars
    def resetAllClipProgressBars(self):
        for i in self.btn_matrix:
            for j in i:
                if j.clip:
                    j.clip.last_offset = 0 # set clip playhead to 0



    # update clip parameter of selected cell
    def updateClipParameterChange(self):
        cell = self.btn_matrix[self.last_clip.x][self.last_clip.y]
        self.updateCellInfo(cell, self.last_clip)





    def onClipNameChange(self):
        self.last_clip.name = self.clip_name.text()
        cell = self.btn_matrix[self.last_clip.x][self.last_clip.y]
        cell.clip_name.setText(self.last_clip.name)
        self.updateClipParameterChange()



    def onClipVolumeChange(self):
        if self.last_clip:
            self.last_clip.volume = common.toAnalogVolumeValue(self.clip_volume.value())
            self.updateClipParameterChange()

            self.labelClipVolume.setText(str(common.toDigitalVolumeValue(self.last_clip.volume)))



    def onBeatDiviserChange(self):
        if self.last_clip:
            self.last_clip.beat_diviser = self.beat_diviser.value()
            self.updateClipParameterChange()


    def onOutputChange(self):
        new_port = self.output.currentText()

        if self.last_clip:
            self.last_clip.output = new_port
            self.updateClipParameterChange()



    def onOneShotClip(self):
        if self.last_clip:
            self.last_clip.one_shot = self.one_shot_clip.isChecked()
            self.updateClipParameterChange()

    def onLockRecord(self):
        if self.last_clip:
            self.last_clip.lock_rec  = self.lock_record.isChecked()
            self.updateClipParameterChange()

    def onAlwaysPlay(self):
        if self.last_clip:
            self.last_clip.always_play = self.always_play_clip.isChecked()
            self.updateClipParameterChange()

    def onMuteGroupChange(self):
        if self.last_clip:
            self.last_clip.mute_group = self.mute_group.value()
            self.updateClipParameterChange()

    def onFrameOffsetChange(self):
        if self.last_clip:
            self.last_clip.frame_offset = self.frame_offset.value()
            self.updateClipParameterChange()

    def onBeatOffsetChange(self):
        if self.last_clip:
            self.last_clip.beat_offset = self.beat_offset.value()
            self.updateClipParameterChange()





    # When adding a port, we also decide if assigning it to current selected clip
    def addPort(self, name, assign = False):
        common.addOutputPort(settings.output_ports,
                             name, 
                             self._jack_client, 
                             self.output_mixer)
        self.updateAudioPorts()

        if self.output.findText(name) == -1:
            self.output.insertItem(self.output.count() - 1, name)
            
        if self.last_clip and assign == True:
            self.last_clip.output = name
            self.output.setCurrentText(name)


    # When removing a port, we also decide to which existing port output routing the clips
    # which were using that output.
    def removePort(self, name, altPort = None):
        common.removeOutputPort(settings.output_ports, 
                                name, 
                                self._jack_client, 
                                self.output_mixer)
        self.updateAudioPorts()                                
        
        # if not specified alternative port name, using default:
        if altPort == None:
            altPort = common.DEFAULT_PORT
        
        for c in self.song.clips:
            if c.output == name:
                c.output = altPort
                
        self.output.removeItem(self.output.findText(name))
        if self.last_clip:
            self.output.setCurrentText(self.last_clip.output)

    def updateAudioPorts(self):
        self.updatePorts.emit()

    def onCopyDetailsClicked(self):
        if self.last_clip:
            self.memory_clip = copy.deepcopy(self.last_clip)
        
    def onPasteDetailsClicked(self):
        if self.last_clip and self.memory_clip:

            self.last_clip.volume = self.memory_clip.volume
            self.last_clip.frame_offset = self.memory_clip.frame_offset
            self.last_clip.beat_offset = self.memory_clip.beat_offset
            self.last_clip.beat_diviser = self.memory_clip.beat_diviser
            self.last_clip.output = self.memory_clip.output
            self.last_clip.mute_group = self.memory_clip.mute_group
            self.last_clip.one_shot = self.memory_clip.one_shot
            self.last_clip.lock_rec = self.memory_clip.lock_rec
            self.last_clip.always_play = self.memory_clip.always_play
            self.last_clip.shot = False
            
            self.updateClipInfo(True)





    # File Menu -------------------------------------------------------------

    def onActionNew(self):
        NewSongDialog(self)

    def getOpenFileName(self, title, file_type, parent=None,
                        dialog=QFileDialog.getOpenFileName):
        path = settings.paths_used.get(file_type, expanduser('~'))
        file_name, a = dialog(parent or self, title, path, file_type)
        if a and file_name:
            if isinstance(file_name, list):
                settings.paths_used[file_type] = dirname(file_name[0])
            else:
                settings.paths_used[file_type] = dirname(file_name)
        return file_name, a

    def getSaveFileName(self, *args):
        return self.getOpenFileName(*args, dialog=QFileDialog.getSaveFileName)

    def onActionOpen(self):
        file_name, a = self.getOpenFileName('Open Song',
                                            common.SONG_FILE_TYPE)  # TODO: const
        if a and file_name and self.checkFileExists(file_name):
            self.openSongFromDisk(file_name)
        else:
            print("File not found or no song selected")
     


    def checkFileExists(self, file_name):
        return isfile(file_name)


    def onActionSave(self):
        if self._jack_client.transport_state == 1 and settings.prevent_song_save == True:
            return

        if self.song.file_name:
            self.song.save()
        else:
            self.onActionSaveAs()

    def getWindowTitle(self, file_name):
        return "SpinTool - {} - {}".format(common.APP_VERSION, file_name)

    def onActionSaveAs(self):
        if self._jack_client.transport_state == 1 and settings.prevent_song_save == True:
            return

        file_name, a = self.getSaveFileName('Save Song', common.SONG_FILE_TYPE)

        if file_name:
            file_name = verify_ext(file_name, common.SONG_FILE_EXT)
            self.song.file_name = file_name
            self.song.save()
            print("File saved to : {}".format(self.song.file_name))
            self.setWindowTitle(self.getWindowTitle(file_name or EMPTY_SONG_NAME))


    def onActionQuit(self):
        self.close()
        #self.onApplicationExit()
        #self.app.quit()



    # MIDI Menu -------------------------------------------------------------

    def onAddDevice(self):
        if self._jack_client.transport_state == 1: # ROLLING

            response = QMessageBox.question(self, "Enter MIDI configuration?", "The song execution will be stopped")
            if response == QMessageBox.No:
                return
            
            self._jack_client.transport_stop()
            self._jack_client.transport_locate(0)        

        
        self.learn_device = LearnDialog(self, self.addDevice)
        self.is_learn_device_mode = True
        self.update()



    def onManageDevice(self):
        ManageDialog(self)


    def onRefresh(self): # -> send init or not?
        # send init + redraw + update
        #self.onDeviceSelect()

        #redraw
        self.redraw()



    # MIDI Menu -------------------------------------------------------------

    def onPreferences(self):
        Preferences(self) # Preferences Dialog

    def onPlaylistEditor(self):
        PlaylistDialog(self)
        self.actionPlaylist_Editor.setEnabled(False)

    def onSceneManager(self):
        self.scenesManagerDialog = SceneManager(self)
        if self.current_scene:
            self.scenesManagerDialog.selectItem(self.getSceneIndex(self.current_scene))
        else:
            self.scenesManagerDialog.selectItem(0)
        self.actionScene_Manager.setEnabled(False)

    def onPortManager(self):
        PortManager(self)
        self.actionPort_Manager.setEnabled(False)

    def onMixer(self):
        if self.output_mixer is None:
            self.output_mixer = Mixer(self)

        self.output_mixer.show()
        self.actionMixer.setEnabled(False)


    def onAction_SongAnnotation(self):
        self.showSongAnnotation()

    def onActionFullScreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
        self.show()



    # Info Menu -------------------------------------------------------------

    def onActionAbout(self):
        About(self)
        
    def onActionWiki(self): 
        QDesktopServices.openUrl(QUrl(common.WIKI_LINK))
        




    def update(self):
    # this also updates midi controllers
        #print("update func")
        for x in range(len(self.song.clips_matrix)):
            line = self.song.clips_matrix[x]
            for y in range(len(line)):
                clp = line[y]
                if clp is None:
                    state = None
                else:
                    state = clp.state

                if state != self.state_matrix[x][y]:
                    if clp:
                        self.btn_matrix[x][y].setColor(state)
                    try:
                        if (settings.slower_processing == True):
                            time.sleep(0.001)
                            
                        self.queue_out.put(self.device.generateNote(x, y, state))

                    except IndexError:
                        # print("No cell associated to %s x %s"
                        # % (clp.x, clp.y))
                        pass

                self.state_matrix[x][y] = state

    def lightDownDevice(self):
        self.device.setAllCellsColor(self.queue_out, self.device.black_vel)
        

    # redraw clip matrix and update device
    def redraw(self):
        self.state_matrix = [[-1 for x in range(self.song.height)]
                             for x in range(self.song.width)]
        self.update()


    def readQueue(self):
        try:
            while True:
                note = self.queue_in.get(block=False)
                if len(note) == 3:
                    status, pitch, vel = struct.unpack('3B', note)
                    channel = status & 0xF
                    msg_type = status >> 4
                    self.processNote(msg_type, channel, pitch, vel)
                    # else:
                    # print("Invalid message length")
        except Empty:
            pass

    def getSceneIndex(self, i_scene):
        index = 0
        for i in range(len(self.device.scene_buttons)):
            if i == i_scene:
                return index
            index += 1
       
        if common.last_gui_triggered_scene:
            return common.last_gui_triggered_scene
       
        return 0            
                    

    # Heart of midi controller note reading (trigger functions with midi controls)
    def processNote(self, msg_type, channel, pitch, vel):

        btn_id = (msg_type, channel, pitch, vel)
        btn_id_vel = (msg_type, channel, pitch, -1)
        ctrl_key = (msg_type, channel, pitch)

        # song volume
        if ctrl_key == self.device.song_volume_ctrl:

            self.song.volume = common.fromControllerAnalogVolume(vel)
            self.updateSongVolumeValue()
            (self.song_volume_knob.setValue(common.toControllerVolumeValue(self.song.volume)))
        
        # PLAY
        elif self.device.play_btn in [btn_id, btn_id_vel]:
            
            self.onPlay()
            
        # PAUSE
        elif self.device.pause_btn in [btn_id, btn_id_vel]:
            
            self.onPause()

        # STOP and rewind
        elif self.device.stop_btn in [btn_id, btn_id_vel]:
            
            self.onStop()

        # REWIND
        elif self.device.rewind_btn in [btn_id, btn_id_vel]:

            self.onRewind()
        
        # GO TO POSITION
        elif self.device.goto_btn in [btn_id, btn_id_vel]:

            self.onGoto()
        
        # RECORD
        elif self.device.record_btn in [btn_id, btn_id_vel]:
            self.onRecord()   # button control color managed in: updateRecordBtn

        # SHIFT
        elif self.device.shift_btn in [btn_id, btn_id_vel]:
            self.onShift()

        # CUSTOM RESET
        elif self.device.custom_reset_btn in [btn_id, btn_id_vel]:
            if self.output_mixer:
                self.output_mixer.onCustomReset()

        # UNLINK MIXER STRIPES
        elif self.device.unlink_stripes_btn in [btn_id, btn_id_vel]:
            self.mixer_stripes_midi_linked = not self.mixer_stripes_midi_linked
            if self.output_mixer:
                self.output_mixer.UpdateStripesLinkGui()

        # Output ports volume control knobs (ex-block line volumes)
        elif ctrl_key in self.device.ctrls and self.mixer_stripes_midi_linked:
            try:
                ctrl_index = self.device.ctrls.index(ctrl_key)
                volume = common.fromControllerAnalogVolume(vel)
                
                # apply change and notify mixer:
                port = common.getOutputPortByIndex(settings.output_ports, ctrl_index)
                if port:
                    settings.output_ports[port]["vol"] = volume

                    if self.output_mixer:
                        self.output_mixer.updateStripVolume(port)

            except KeyError:
                pass


        # Output ports send1 control knobs
        elif ctrl_key in self.device.send1ctrls and self.mixer_stripes_midi_linked:
            try:
                ctrl_index = self.device.send1ctrls.index(ctrl_key)
                send1 = common.fromControllerAnalogVolume(vel)

                # apply change and notify mixer:
                port = common.getOutputPortByIndex(settings.output_ports, ctrl_index)
                if port:
                    settings.output_ports[port]["send1"] = send1

                    if self.output_mixer:
                        self.output_mixer.updateStripSend1(port)

            except KeyError:
                pass


        # Output ports send2 control knobs
        elif ctrl_key in self.device.send2ctrls and self.mixer_stripes_midi_linked:
            try:
                ctrl_index = self.device.send2ctrls.index(ctrl_key)
                send2 = common.fromControllerAnalogVolume(vel)

                # apply change and notify mixer:
                port = common.getOutputPortByIndex(settings.output_ports, ctrl_index)
                if port:
                    settings.output_ports[port]["send2"] = send2

                    if self.output_mixer:
                        self.output_mixer.updateStripSend2(port)

            except KeyError:
                pass

            
        # Scenes
        elif (btn_id in self.device.scene_buttons
              or btn_id_vel in self.device.scene_buttons):
            try:
                scene_id = self.device.scene_buttons.index(btn_id)
                self.current_scene = (self.device.scene_buttons.index(btn_id))
            except ValueError:
                scene_id = self.device.scene_buttons.index(btn_id_vel)
                self.current_scene = (self.device.scene_buttons.index(btn_id_vel))
            
            shifted = False

            # if Shift was pressed, scene id is incremented by scenes number 
            # (e.g. if 5 scenes buttons were configured and button of scene 2 was pressed with shift active,
            # scene 7 is launched)
            if self.shift_active:
                shifted = True
                scene_id = scene_id + len(self.device.scene_buttons)

                if settings.disable_shift_after_processing == True:
                    self.onShift() # unactivating shift function and related midi button

            sceneExhists = True

            try:
                self.song.loadSceneId(scene_id)
                self.update()

            except IndexError:
                print('cannot load scene {} - there are only {} scenes.'
                      ''.format(scene_id, len(self.song.scenes)))
                sceneExhists = False

            if sceneExhists == True:
                # buttons are updated and scene button is lighted on just if scene exhists:
                for i in range(len(self.device.scene_buttons)):
                    (a, b_channel, b_pitch, b) = self.device.scene_buttons[i]
                    if i == self.current_scene:
                        if shifted == False:
                            # Green for un-shifted scene (button number == scene number)
                            color = self.device.green_vel
                            sceneToSelect = self.current_scene
                        else:
                            # Green blink for shifted scene (button number == scene number - scenes total buttons)
                            color = self.device.blink_green_vel
                            sceneToSelect = self.current_scene + len(self.device.scene_buttons)
                    else:
                        color = self.device.black_vel
                        
                    self.queue_out.put(((self.NOTEON << 4) + b_channel, b_pitch, color))
                    time.sleep(0.01)
                
                # If scene dialog visible, updating selected scene
                if self.scenesManagerDialog:
                    self.scenesManagerDialog.selectItem(sceneToSelect)


        # Mute output ports (ex-Line blocks)
        elif (btn_id in self.device.mute_buttons
              or btn_id_vel in self.device.mute_buttons) and self.mixer_stripes_midi_linked:
            try:
                mute_button = (self.device.mute_buttons.index(btn_id))
            except ValueError:
                mute_button = (self.device.mute_buttons.index(btn_id_vel))

            
            # apply change and notify mixer:
            port = common.getOutputPortByIndex(settings.output_ports, mute_button)
            if port:
                settings.output_ports[port]["mute"] = not settings.output_ports[port]["mute"]

                if self.output_mixer:
                    self.output_mixer.updateStripMute(port)

                for i in range(len(self.device.mute_buttons)):
                    (a, b_channel, b_pitch, b) = self.device.mute_buttons[i]
                    if i == mute_button:
                        if settings.output_ports[port]["mute"] == True:
                            color = self.device.red_vel                                
                        else:
                            color = self.device.black_vel
                        self.queue_out.put(((self.NOTEON << 4) + b_channel, b_pitch, color))
                        break
        
        # Start / Stop clips
        else:
            x, y = -1, -1
            try:
                x, y = self.device.getXY(btn_id)
            except IndexError:
                pass
            except KeyError:
                try:
                    x, y = self.device.getXY(btn_id_vel)
                except KeyError:
                    pass

            # start/stop clip
            if (x >= 0 and y >= 0):
                # trigger clip
                if not self.shift_active:
                    self.startStop(x, y, True)
                # force clip
                else:
                    self.btn_matrix[x][y].force_clip_start_stop()
                    if settings.disable_shift_after_processing == True:
                        self.onShift() # unactivating shift function and related midi button                    


    def updateMidiPause(self):

        if not self.device:
            return

        if self.device.stop_btn:
            (a, b_channel, b_pitch, b) = self.device.stop_btn
            note = ((a << 4) + b_channel, b_pitch, self.device.black_vel)
            self.queue_out.put(note)

        if self.device.play_btn:
            (a, b_channel, b_pitch, b) = self.device.play_btn
            note = ((a << 4) + b_channel, b_pitch, self.device.black_vel)
            self.queue_out.put(note)
        
        if self.device.pause_btn:
            (a, b_channel, b_pitch, b) = self.device.pause_btn

            if settings.rec_color == settings.COLOR_AMBER:
                color = self.device.red_vel
            else:
                color = self.device.amber_vel
            note = ((a << 4) + b_channel, b_pitch, color)
            self.queue_out.put(note) 

    def updateMidiStop(self):

        if not self.device:
            return

        if self.device.pause_btn:
            (a, b_channel, b_pitch, b) = self.device.pause_btn
            note = ((a << 4) + b_channel, b_pitch, self.device.black_vel)
            self.queue_out.put(note)

        if self.device.play_btn:
            (a, b_channel, b_pitch, b) = self.device.play_btn
            note = ((a << 4) + b_channel, b_pitch, self.device.black_vel)
            self.queue_out.put(note)
        
        if self.device.stop_btn:
            (a, b_channel, b_pitch, b) = self.device.stop_btn

            if settings.rec_color == settings.COLOR_AMBER:
                color = self.device.red_vel
            else:
                color = self.device.amber_vel
            note = ((a << 4) + b_channel, b_pitch, color)
            self.queue_out.put(note)

    def updateMidiPlay(self):

        if not self.device:
            return

        if self.device.play_btn:
            (a, b_channel, b_pitch, b) = self.device.play_btn
            note = ((a << 4) + b_channel, b_pitch, self.device.green_vel)
            self.queue_out.put(note)
        
        if self.device.pause_btn:
            (a, b_channel, b_pitch, b) = self.device.pause_btn
            note = ((a << 4) + b_channel, b_pitch, self.device.black_vel)
            self.queue_out.put(note)

        if self.device.stop_btn:
            (a, b_channel, b_pitch, b) = self.device.stop_btn
            note = ((a << 4) + b_channel, b_pitch, self.device.black_vel)
            self.queue_out.put(note)

    # called usually from Mixer: to update a mute button on MIDI controller
    def updateMidiMute(self, port, index):

        if not self.device:
            return
        
        if (index + 1) > len(self.device.mute_buttons):
            return

        if self.device.mute_buttons[index]:
            (a, b_channel, b_pitch, b) = self.device.mute_buttons[index]

            if settings.output_ports[port]["mute"] == True:
                color = self.device.red_vel                                
            else:
                color = self.device.black_vel
            self.queue_out.put(((self.NOTEON << 4) + b_channel, b_pitch, color))

    # called usually from Mixer: to reset all mute buttons on MIDI controller
    def resetMidiMute(self):

        if not self.device:
            return
        
        if not self.device.mute_buttons:
            return

        for i in range(len(self.device.mute_buttons)):
            (a, b_channel, b_pitch, b) = self.device.mute_buttons[i]
            self.queue_out.put(((self.NOTEON << 4) + b_channel, b_pitch, self.device.black_vel))

    # called usually when activating: a Scene from Scene Manager: to update scenes buttons on MIDI controller
    def updateScene(self, scene, sceneIndex):
        
        if not self.device:
            return

        self.current_scene = scene
        common.last_gui_triggered_scene = sceneIndex
        self.update()

        if not self.device.scene_buttons:
            return

        # Row Index starts from 0, so row NUMBER is Row Index + 1
        if (sceneIndex + 1) > len(self.device.scene_buttons):
            shifted = True
            sceneColor = self.device.blink_green_vel
        else:
            shifted = False
            sceneColor = self.device.green_vel

        # buttons are updated and scene button is lighted on
        for i in range(len(self.device.scene_buttons)):
            (a, b_channel, b_pitch, b) = self.device.scene_buttons[i]

            if (shifted == False and i == sceneIndex) or \
               (shifted == True and i == (sceneIndex - len(self.device.scene_buttons))):
                color = sceneColor
            else:
                color = self.device.black_vel
                
            self.queue_out.put(((self.NOTEON << 4) + b_channel, b_pitch, color))
            time.sleep(0.01)

    def updateScenesButtons(self, scene):
        if self.device and scene:

            if not self.device.scene_buttons:
                return
            
            index = 0
            for i, enScene in enumerate(self.song.scenes):
                if enScene == scene:
                    index = i

            for i in range(len(self.device.scene_buttons)):
                (a, b_channel, b_pitch, b) = self.device.scene_buttons[i]
                if index == i:  
                    color = self.device.green_vel 
                else:
                    color = self.device.black_vel
                self.queue_out.put(((self.NOTEON << 4) + b_channel, b_pitch, color))

    def toggleBlinkButton(self):
        for line in self.btn_matrix:
            for btn in line:
                if btn.blink:
                    if self.blktimer.state:
                        btn.setStyleSheet(btn.color)
                    else:
                        btn.setStyleSheet(self.DEFAULT)
        if self.song.is_record:
            if self.blktimer.state:
                self.recordButton.setStyleSheet(self.RECORD_BLINK)
            else:
                self.recordButton.setStyleSheet(self.RECORD_DEFAULT)

        self.blktimer.state = not self.blktimer.state



    def updateProgress(self):
        state, pos = self._jack_client.transport_query()
        if 'bar' in pos:
            bbt = "%d|%d|%03d" % (pos['bar'], pos['beat'], pos['tick'])
        else:
            bbt = "-|-|-"
        seconds = int(pos['frame'] / pos['frame_rate'])
        (minutes, second) = divmod(seconds, 60)
        (hour, minute) = divmod(minutes, 60)
        time = "%d:%02d:%02d" % (hour, minute, second)
        self.bbtLabel.setText("%s\n%s" % (bbt, time))
        for line in self.btn_matrix:
            for btn in line:
                if btn.clip and btn.clip.audio_file:
                    value = ((btn.clip.last_offset
                              / self.song.length(btn.clip))
                             * 97)
                    btn.clip_position.setValue(value)
                    btn.clip_position.repaint()


    def updateDevices(self):
        #print("update devices")
        for action in self.deviceGroup.actions():
            self.deviceGroup.removeAction(action)
            self.menuDevice.removeAction(action)
        for device in self.devices:
            action = QAction(device.name, self.menuDevice)
            action.setCheckable(True)
            action.setData(device)
            self.menuDevice.addAction(action)
            self.deviceGroup.addAction(action)
        action.setChecked(True)
        self.device = device


    def addDevice(self, device):
        self.devices.append(device)
        self.updateDevices()
        self.is_learn_device_mode = False


    def onDeviceSelect(self):
        self.device = self.deviceGroup.checkedAction().data()
        if self.device:
            # send init command
            if self.device.init_command:
                for note in self.device.init_command:
                    self.queue_out.put(note)
            self.redraw()

        

    def timebase_callback(self, state, nframes, pos, new_pos):
        if pos.frame_rate == 0:
            return None
        pos.valid = 0x10
        pos.bar_start_tick = BAR_START_TICK
        pos.beats_per_bar = self.beat_per_bar.value()
        pos.beat_type = BEAT_TYPE
        pos.ticks_per_beat = TICKS_PER_BEAT
        pos.beats_per_minute = self.bpm.value()
        ticks_per_second = (pos.beats_per_minute *
                            pos.ticks_per_beat) / 60
        ticks = (ticks_per_second * pos.frame) / pos.frame_rate
        (beats, pos.tick) = divmod(int(round(ticks, 0)),
                                   int(round(pos.ticks_per_beat, 0)))
        (bar, beat) = divmod(beats, int(round(pos.beats_per_bar, 0)))
        (pos.bar, pos.beat) = (bar + 1, beat + 1)
        return None
