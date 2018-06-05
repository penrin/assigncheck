assigncheck
===========

This make voice file to check connected loudspeaker's assignments.
The audio is made with the macOS `say` command.


Requirements
------------

* macOS 10.7
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
At this time, it is recommended to choose easy-to-hear voice.
You can check the voice list by

* command `say -v '?'`
* System Preference > Accessibility > Speech > System Voice


If you want to get monaural wave files, do

```
$ python assigncheck.py -n 12 --voice Ava --split
```



```
$ python assigncheck.py -h
usage: assigncheck.py [-h] -n N [-o O] [-t T] [-r R] [-w W] [-s] [-v VOICE]


optional arguments:
  -h, --help            show this help message and exit
  -n N                  number of channels
  -o O                  output filename
  -t T                  interval (sec), default=1
  -r R                  sample rate (Hz), default=48000
  -w W                  sample width (Byte), default=3
  -s, --split           split to mono
  -v VOICE, --voice VOICE
                        voice name (you can search with $ say -v '?')
```





