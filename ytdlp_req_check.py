#!/usr/bin/env python
''' use the script to check if dependencies for ytdlp.py
exists on system'''

import os
import importlib.util
from importlib.metadata import version
from shutil import which
from subprocess import run

# set requirements to check here
libs = ['yt_dlp', 'yt_dlp_ejs', 'mutagen'] 	# python libs
exe1 = ['ffmpeg', 'ffprobe']				# fftools!!!, .exe in the same folder as script
exe2 = ['deno']								# installed on system

ok = {}
not_ok = []

# checking python libs
for lib in libs:
	if importlib.util.find_spec(lib) is None:
		not_ok.append('[LIB] '+lib)
	else:
		ok['[LIB] '+lib] = version(lib)

# getting path of this script, assumes ffmpeg and ffprobe exists in the same folder
script_dir = os.path.dirname(os.path.realpath(__file__))

# checking exe1
for exe in exe1:
	if bool(os.path.exists(script_dir+Rf'\{exe}.exe')):
		exe_version = run([exe, '-version'], capture_output=True, text=True).stdout
		vers = ''.join(char for char in exe_version)
		vers = vers.split(' Copyright')
		vers = vers[0].split('version ')
		vers = vers[1]
		ok['[EXE] '+exe] = vers
	else:
		not_ok.append('[EXE] '+exe)

# checking exe2 with shutil's which
for exe in exe2:
	if bool(which(exe)):
		exe_version = run([exe, '-version'], capture_output=True, text=True).stdout
		vers = ''.join(char for char in exe_version)
		vers = vers.strip('\n')
		vers = vers.split('deno ')
		vers = vers[1]
		ok['[EXE] '+exe] = vers
	else:
		not_ok.append(exe)

# report func to be called from ytdlp.py, will not work if called from py console
# returns true if any requirements are not found
def report():
	return bool(not_ok)

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
	if ok:
		print2(color(GREEN, 'found >>'),
			color(YELLOW, f'  \033[4m[typ] {"name":<14} version\033[24m'))
		for k, v in ok.items():
			print2(f'  {k:<20} {v}')

	if not_ok:
		print2(color(RED_BG, 'not found >>'))
		for item in not_ok:
			print2(f'  {item}')

if __name__ == '__main__':
	main()