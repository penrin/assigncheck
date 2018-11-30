import sys
import os
import time
import argparse
import wave
from subprocess import Popen
import numpy as np


def readwav(filename):
    wr = wave.open(filename, 'r')
    params = wr.getparams()
    nchannels = params[0]
    sampwidth = params[1]
    rate = params[2]
    nframes =  params[3]
    frames = wr.readframes(nframes)
    wr.close()

    # binary -> int
    if sampwidth == 2:
        data = np.frombuffer(frames, dtype=np.int16)
    elif sampwidth == 3:
        a8 = np.fromstring(frames, dtype=np.uint8)
        tmp = np.empty((nframes, nchannels, 4), dtype = np.uint8)
        tmp[:, :, :sampwidth] = a8.reshape(-1, nchannels, sampwidth)
        tmp[:, :, sampwidth:] = (tmp[:, :, sampwidth - 1:sampwidth] >> 7) * 255
        data = tmp.view('int32')
    elif sampwidth == 4:
        data = np.frombuffer(frames, dtype=np.int32)
    
    # Mold: numpy array (nframes, nchannels), -1.0 ≤ sample < 1.0
    data = data.astype(float) / 2 ** (8 * sampwidth - 1)
    data = np.reshape(data, (-1, nchannels))
    return data

def writewav(filename, data, ws=3, fs=48000):
    nchannels = data.shape[1]
    sampwidth = ws
    data = (data * (2 ** (8 * sampwidth - 1) - 1)).reshape(data.size, 1)
    
    if sampwidth == 2:
        frames = data.astype(np.int16).tostring()
    elif sampwidth == 3:
        a32 = np.asarray(data, dtype = np.int32)
        a8 = (a32.reshape(a32.shape + (1,)) >> np.array([0, 8, 16])) & 255
        frames = a8.astype(np.uint8).tostring()
    elif sampwidth == 4:
        frames = data.astype(np.int32).tostring()
    
    w = wave.open(filename, 'wb')
    w.setparams((nchannels, sampwidth, fs, 0, 'NONE', 'not compressed'))
    w.writeframes(frames)
    w.close()
    return

def progressbar(percent, end=1, bar_length=40, slug='#', space='-'):
    percent = percent / end # float
    slugs = slug * int( round( percent * bar_length ) )
    spaces = space * ( bar_length - len( slugs ) )
    bar = slugs + spaces
    sys.stdout.write("\r[{bar}] {percent:.1f}% ".format(
    	bar=bar, percent=percent*100.
    ))
    sys.stdout.flush()
    if percent == 1:
        print()


parser = argparse.ArgumentParser()
parser.add_argument('-n', type=int, help='number of channels', required=True)
parser.add_argument('-o', type=str, default='out', help='output filename')
parser.add_argument('-t', type=float, default=1., help='interval (sec), default=1')
parser.add_argument('-r', type=int, default=48000, help='sample rate (Hz), default=48000')
parser.add_argument('-w', type=int, default=2, help='sample width (Byte), default=2')
parser.add_argument('-g', type=float, default=0., help='gain (dB), default=0')
parser.add_argument('-s', '--split', action='store_true', help='split to mono')
parser.add_argument('-v', '--voice', type=str, help='voice name (you can search with $ say -v \'?\')')
args = parser.parse_args()

num_channels = args.n
interval_second = args.t
samplerate = args.r
samplewidth = args.w
gain = 10 ** (args.g / 20)
interval = int(samplerate * interval_second)


## Speech synthesis with 'Say'
data = []
workfilename = 'WORKFILE%f.wav' % time.time()
print('Synthesis...')
for i in range(num_channels):
    progressbar(i, num_channels)
    channel = i + 1
    cmd = '/usr/bin/say -o %s --data-format=LEI%d@%d'\
            % (workfilename, samplewidth * 8, samplerate)
    if args.voice != None:
        cmd += ' -v %s' % args.voice
    cmd += ' %d' % channel
    proc = Popen(cmd, shell=True)
    proc.wait()
    
    data.append(readwav(workfilename).reshape(-1))
progressbar(1)
os.remove(workfilename)


## Combine
print('Editing...', end=''); sys.stdout.flush()

len_output = 0
for i in range(num_channels):
    endtime = data[i].shape[0] + interval * i
    if len_output < endtime:
        len_output = endtime
data_multi = np.zeros([num_channels, len_output])

for i in range(num_channels):
    end1 = interval * i
    end2 = end1 + data[i].shape[0]
    data_multi[i, end1:end2] = data[i]

data_multi *= gain

print('Done')


## limit amplitude
if np.max(np.abs(data_multi)) > 1.:
    satu_max =  20 * np.log10(np.max(np.abs(data_multi)))
    print('%.1f dB saturation detected!' % satu_max, end='')
    
    # limiter
    threshold = 1.
    i_satu = np.where(np.abs(data_multi) > threshold)
    data_multi[i_satu] = np.sign(data_multi[i_satu]) * threshold
    print(' --> limited to 0 dBFS' % satu_max)


## Write
print('Writing...', end=''); sys.stdout.flush()

if args.split == True:
    
    digit = len(str(num_channels))
    for i in range(num_channels):
        outfilename = '%s_%s.wav' % (args.o, str(i + 1).zfill(digit))
        writewav(outfilename, data_multi[i, :].reshape(-1, 1),
                ws=samplewidth, fs=samplerate)
else:
    outfilename = '%s.wav' % args.o
    writewav(outfilename, data_multi.T, ws=samplewidth, fs=samplerate)

print('Done')



