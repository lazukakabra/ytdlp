#!/usr/bin/env python
''' use the script to check if dependencies for ytdlp.py
exists on system'''

import os
from shutil import which
import importlib.util

# foreground color codes
os.system('color') # needed for ANSI color codes to work (win10)
RED, GREEN, YELLOW, CYAN = '\033[91m', '\033[92m', '\033[93m', '\033[96m'
RESET = '\033[0m'  # This resets the color back to default

# color input and reset cmd style to default
def color(color:str, arg:str) -> str:
	return color+arg+RESET

# \t, indented print
def print2(*arg):
	for element in arg:
		print(f'\t{element}')


print2(color(CYAN, f'detected OS >> ')+os.name)

# import block
try:
	import yt_dlp
	print2(color(GREEN, f'{"yt-dlp":<16}ok'))
except ImportError as e:
	if type(e) == ModuleNotFoundError:
		print2(color(RED, 'yt-dlp not installed, use "pip install yt_dlp"'))
	else:
		print2(color(RED, 'error importing yt-dlp: ')+e)
	quit()

if importlib.util.find_spec('yt_dlp_ejs') is None:
	print2(color(RED, 'yt-dlp-ejs not installed, use "pip install yt-dlp-ejs'))
else:
	print2(color(GREEN, f'{"yt-dlp-ejs":<16}ok'))

if importlib.util.find_spec('mutagen') is None:
	print2(color(RED, 'mutagen not installed, use "pip install mutagen'))
else:
	print2(color(GREEN, f'{"mutagen":<16}ok'))

# check if ffmpeg, deno etc. are installed, will look for ffmpeg tools
# in the same folder as this script. change if nescessary etc.
script_dir = os.path.dirname(os.path.realpath(__file__))
#script_dir = your_path

ffmpeg_exists = bool(os.path.exists(script_dir+R'\ffmpeg.exe'))
ffprobe_exists = bool(os.path.exists(script_dir+R'\ffprobe.exe'))
deno_exists = bool(which('deno'))

requirements = {'ffmpeg':ffmpeg_exists, 'ffprobe':ffprobe_exists, 'deno':deno_exists}

def exists(name:str, value:bool)->int:
	if not value:
		print2(color(RED, f'{name} \tnot found'))
		return 1
	else:
		print2(color(GREEN, f'{name:<16}ok'))
		return 0

err_sum = 0
for key, val in requirements.items():
	err_sum += exists(key, val)

if err_sum > 0:
	print2('missing requirements, exiting...')
	quit()

