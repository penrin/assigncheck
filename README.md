assigncheck
===========

A tool to make audio file that reads numbers in order,
used for checking the connection of multi-channel playback system.
The audio is made with the macOS `say` command.

![likethis](https://user-images.githubusercontent.com/8520833/49262953-fa31cf80-f48b-11e8-82f6-11b7e7e4b956.png)

Requirements
------------

* macOS 10.7 or Later
* python3
* numpy


Installation
------------

```
$ git clone https://github.com/penrin/assigncheck
```

Usage
-----
```
$ python assigncheck.py -n 12 --voice Ava
```
make a wave file with the number of tracks specified by option `-n`.


You can choose the type of voice by option `-v`. It is recommended to choose easy-to-hear voice.
You can check the voice list by the following method.

* command `say -v '?'`
* System Preference > Accessibility > Speech > System Voice


If you want to get monaural wave files, do

```
$ python assigncheck.py -n 12 --voice Ava --split
```


Help:

```
$ python assigncheck.py -h
usage: assigncheck.py [-h] -n N [-o O] [-t T] [-r R] [-w W] [-s] [-v VOICE]


optional arguments:
  -h, --help            show this help message and exit
  -n N                  number of channels
  -o O                  output filename
  -t T                  interval (sec), default=1
  -r R                  sample rate (Hz), default=48000
  -g G                  gain (dB), default=0
  -w W                  sample width (Byte), default=2
  -s, --split           split to mono
  -v VOICE, --voice VOICE
                        voice name (you can search with $ say -v '?')
```






