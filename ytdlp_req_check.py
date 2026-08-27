#!/usr/bin/env python
''' use the script to check if dependencies for ytdlp.py
exists on system'''

import os
from importlib.util import find_spec
from importlib.metadata import version
from shutil import which
from subprocess import run

# set requirements to check here
libs = ['yt_dlp', 'yt_dlp_ejs', 'mutagen']	# python libs
exe1 = ['ffmpeg', 'ffprobe']	# fftools gives alot of version info, separated
exe2 = ['deno']	# installed on system

status = {}
not_found = 0

# checking python libs
for lib in libs:
	if find_spec(lib) is None:
		not_found += 1
		status['[LIB] '+lib] = 'not found'
	else:
		status['[LIB] '+lib] = version(lib)

# checking exe1
for exe in exe1:
	if bool(which(exe)):
		exe_version = run([exe, '-version'], capture_output=True, text=True).stdout
		vers = ''.join(char for char in exe_version)
		vers = vers.split(' Copyright')
		vers = vers[0].split('version ')
		vers = vers[1]
		status['[EXE] '+exe] = vers
	else:
		not_found += 1
		status['[EXE] '+exe] = 'not found'

# checking exe2 with shutil's which
for exe in exe2:
	if bool(which(exe)):
		exe_version = run([exe, '-version'], capture_output=True, text=True).stdout
		vers = ''.join(char for char in exe_version)
		vers = vers.strip('\n')
		vers = vers.split('deno ')
		vers = vers[1]
		status['[EXE] '+exe] = vers
	else:
		not_found += 1
		status['[EXE] '+exe] = 'not found'

# report func to be called from ytdlp.py, will not work if called from py console
# returns true if any requirements are not found
def report():
	return bool(not_found)

def main():
	# foreground color codes
	os.system('color') # needed for ANSI color codes to work (win10)
	GREEN, YELLOW, DARK_CYAN, RED_BG = '\033[92m', '\033[93m', '\033[36m', '\033[41m'
	RESET = '\033[0m'  # This resets the color back to default

	# color input and reset cmd style to default
	def color(color:str, arg:str) -> str:
		return color+arg+RESET

	# \t, indented print
	def print2(*arg):
		for element in arg:
			print(f'\t{element}')

	# get OS, because why not
	print2(color(DARK_CYAN, f'detected OS >> ')+os.name)

	# printing status msgs
	header = color(YELLOW, f'{"[state]":<11}[typ] {"name":<14} version')
	separater_row = ''.join('-' for _ in range(len(header)))
	print2(separater_row, header, separater_row)
	for pkg, state in status.items():
		if state == 'not found':
			print2(f'{color(RED_BG, '[- FOUND]'):<11}'+f'  {pkg}')
		else:
			print2(f'{color(GREEN, '[+ FOUND]'):<11}'+f'  {pkg:<20} {state}')
	print2(separater_row)

if __name__ == '__main__':
	main()