# SuperBoucle

Hi everyone! SuperBoucle is a loop based software fully controllable with any 
midi device, synced with Jack transport. This version derives from original 
Vampouille's SuperBoucle, starting from a fork of the original repository.

See "readme-language.md" for details and usage manual (not up-to-date...
a Wiki section will be available soon)

Note: I never developed in Python until now and I never developed anything
on Linux in general. I tried, beacuse I needed some extra features, and this 
is the result... I made some intensive testing and it seems stable to me.
This means that perhaps code could be improved furtherly and that some more
functions could be added in future, when I'll be more skilled, if I'll have
the time to. Enjoy!

## Features

* Jack Transport
* Record
* Auto record latency
* Audio input / output
* Midi input / output
* Normalize and revert samples
* Negative sample offset, sample offset in beats or frames
* Load several formats: WAV, FLAC, AIFF, ...  (no MP3 at the moment)
* Full intuitive MIDI learn interface
* Support any MIDI device: generic keyboard, pad, BCF, Akai APC, ...
* Fully controllable by MIDI device or mouse/keyboard
* "Go to" function to move jack transport to specified location

## What's new

A bunch of issues were fixed, and some features were added.
Especially:

* One-shot clips
* Light-on all midi device buttons (scenes and transport too)
* Preferences Window
* Start a clip just after recording it
* Show clip details when triggered for start/stop
* Show clip details when its volume is changed from controller
* Preferred grid size, to match your controller's buttons grid
* Choice of clip recording color (amber is default, red available)
* Open scenes and playlist windows on start up

New versioning starts from 20.04.07

## Requirements

### Linux

* Python 3
* Pip for python 3
* Python modules : Cffi, PySoundFile, Numpy, PyQT 5
* Running jack server

Recommended:
* a2jmidid to access midi controller
* Carla to save connections

### Windows

I still have to decide if produce a Windows setup package too

## Installation

### Linux

* Install Jack server :

        sudo aptitude install jackd2 qjackctl

* Install midi bridge (optional) : 

        sudo aptitude install a2jmidid

* Install python modules : 

        sudo aptitude install python3 python3-pip python3-cffi python3-numpy python3-pyqt5
        sudo pip3 install PySoundFile

* Download and extract last version of SuperBoucle from https://github.com/Vampouille/superboucle/releases/

## Running

### Linux

Start Jack audio server and then run SuperBoucle.sh script from SuperBoucle directory :

	./SuperBoucle.sh

## Credits and links

I have to thank first of all Vampouille, who created SuperBoucle and fixed some
issues I reported, and Vince who helped me understanding how to start and proceed
in my development.
Original SuperBoucle master repository is here: 
	https://github.com/Vampouille/superboucle
and Vince activities website:
	https://www.sonejo.net/

