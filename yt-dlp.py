#!/usr/bin/env python
'''
requirements and made with versions:
[exe] python 3.14.6, deno 2.9.4
[exe] ffmpeg 2026-07-30-git-2ae2413488-full_build-www.gyan.dev
[exe] ffprobe 2026-07-30-git-2ae2413488-full_build-www.gyan.dev
[lib] yt-dlp 2026.7.4, yt-dlp-ejs 0.8.0, mutagen 1.48.1-py3

assumes ffmpeg and ffprobe are in the same folder

use devscripts/cli_to_api.py to translate cli arguments to ydl_opts code.
'''

import os
from shutil import move
import tempfile
import yt_dlp
import ytdlp_req_check as yrc

# foreground color codes
os.system('color') # needed for ANSI color codes to work (win10)
GREEN = '\033[92m'
YELLOW = '\033[38;5;226m'
DARK_CYAN = '\033[36m'
RED_BG = '\033[41m'
MAGENTA = '\033[38;5;201m'
ORANGE = '\033[38;5;209m'
TURQUOISE = '\033[38;5;50m'
RESET = '\033[0m'  # This resets the color back to default

# color wrapping
def color(color, arg:str)->str:
	return color+arg+RESET

# \t, indented print
def print2(*arg):
	for element in arg:
		print(f'\t{element}')

# create directory and print location
def create_dir(path:str):
	if not os.path.exists(path):
		os.mkdir(path)
		print2(color(DARK_CYAN, 'folder created at: ')+f'{path}')

# downloader function, needs url, 'audio' or 'video', tmp folder path
def download(youtube_url:str, output_dir:str, audio_or_video:str):
	# video options
	ydl_opts_video = {
		'cookiesfrombrowser': ('firefox', None, None, None),
		'format': 'bestvideo+bestaudio/best',
        'outtmpl': f'{output_dir}/%(uploader_id)s - %(title)s.%(ext)s',
        'quiet': True,
        'merge_output_format': 'mp4',
		}

	# audio options
	ydl_opts_audio = {
		'format': 'opus/bestaudio/best',
        'outtmpl': f'{output_dir}/%(uploader_id)s--SEP--%(uploader)s--SEP--%(title)s.%(ext)s',
        'quiet': True,
        'postprocessors': [
        	{'key':'FFmpegExtractAudio', 'preferredcodec':'opus'},
        	{'key':'FFmpegMetadata', 'add_metadata':True, 'add_metadata': True,},
        	{'key':'EmbedThumbnail'}],
        'writethumbnail': True,
		}

	ydl_opts_list = {'video':ydl_opts_video, 'audio':ydl_opts_audio}

	# download file
	with yt_dlp.YoutubeDL(ydl_opts_list[audio_or_video]) as ydl:
		try:
			ydl.download([youtube_url])
			print2(color(GREEN, 'downloaded'), os.listdir(output_dir)[0], '')
			return True
		except Exception as e:
			#print2('error occured: ', e)
			return False

# fix filename and move to set directories 
def rename_and_move(dl_dir:str, tmp_dir:str, vid_or_aud:str):
	# change working directory to tmp_dir and get filename
	# old_filename used for status msg
	prev_dir = os.getcwd()
	os.chdir(tmp_dir)
	old_filename = os.listdir()[0]
	filename = old_filename

	# removing @ symbol from uploader_id
	if filename[0] == '@':
		filename = filename[1:]
		print2('removed '+color(MAGENTA, '@')+' from uploader_id in filename')	

	# if vid_or_aud = 'audio' then change dl_dir to save file in dl_dir\uploader_id
	# --SEP-- is added when dl audio, see "ydl_opts_audio" in download()
	# determine uploader name to use, preferred is uploader_id which 
	# can return NA, if so -> use 'uploader' and
	# remove ' - topic' if present from filename 
	if vid_or_aud == 'audio':
		filename_split = filename.split('--SEP--')
		filename = filename_split[-1]
		if filename_split[0] == 'NA':
			uploader_id = filename_split[1]
			if uploader_id[-8:] == ' - Topic':
				uploader_id = uploader_id[:-8]
		else:
			uploader_id = filename_split[0]

		dl_dir = os.path.join(dl_dir, uploader_id)
		create_dir(dl_dir)

	# check if filename exists in destination directory
	def check_duplicate(name:str, og_name:str, directory:str, n=1):
		path_dupe = os.path.join(directory, name)
		extension = len(name.split('.')[-1])+1
		if os.path.exists(path_dupe):
			name = og_name[:-extension] + f' ({n}){og_name[-extension:]}'
			name, n = check_duplicate(name, og_name, directory, n+1)
		return name, n

	# checking for duplicates in dl_dir
	filename, n_duplicate = check_duplicate(filename, filename, dl_dir)
	print2(f'found '+color(MAGENTA, f'{n_duplicate-1}')+' duplicates in destination folder', '')

	# renaming file
	os.rename(old_filename, filename)
	print2(color(GREEN,'renamed'),'from: '+old_filename, '  to: '+filename, '')

	# joining paths to avoid '\' issues
	old_file_path = os.path.join(tmp_dir, filename)
	new_file_path = os.path.join(dl_dir, filename)

	# moving file
	move(old_file_path, new_file_path)
	print2(color(GREEN, f'moved >> {filename}'), 'from: '+tmp_dir,
		'  to: '+dl_dir, '')

	# move back to prev dir to safely delete temporary directory
	os.chdir(prev_dir)

# main dl loop, needs 2 paths and either 'video' or 'audio'
def download_loop(dl_dir:str, vid_or_aud:str):
	c = {'video': TURQUOISE, 'audio': ORANGE}
	while True:
		url = input(color(c[vid_or_aud], f'    [{vid_or_aud.upper()}] >> enter url or leave empty to return to start. '))

		# if no url return
		if not url:
			return

		# download_...() returns True if download successful, then rename file
		with tempfile.TemporaryDirectory() as temp_dir:
			download_ok = download(url, temp_dir, vid_or_aud)
			if download_ok:
				rename_and_move(dl_dir, temp_dir, vid_or_aud)

# gets download folder paths from file if it exists, creates file if it does not
def check_file_for_paths(filename:str)->dict:
	# if file doesnt exist, create it and add file save locations
	script_dir = os.path.dirname(os.path.realpath(__file__))
	prv_dir = os.getcwd()
	os.chdir(script_dir)
	if not os.path.exists(filename):
		print2('[ATTN] >> file containing save locations '+color(RED_BG, 'not')+' found, creating...')
		locations = {}
		while True:
			locations['video'] = input('\t[INPUT] >> enter location to save videos, full path: ')
			locations['audio'] = input('\t[INPUT] >> enter location to save audios, full path: ')
			for k,v in locations.items():
				print2('\t  '+k+': '+v)
			q = input('\t[INPUT] >> is the above folders correct? [Y/n] ')
			if q and str(q).lower() not in ['y', 'ye', 'yes']:
				continue
			break

		# write to file the entered locations
		with open(filename, 'x') as f:
			for k, v in locations.items():
				f.write(k+' = '+v + '\n')
		print2(color(GREEN, 'created file >> ')+filename)

	# get file paths from filename
	locs = {}
	with open(filename) as f:
		contents = f.read()
	for line in contents.split('\n'):
		if not line: continue
		k, v = line.split(' = ')
		locs[k] = v

	# print locations and return dict
	print2(color(GREEN, 'found ')+f'{filename}, '
		+color(DARK_CYAN, 'download folders set to:'),
		color(DARK_CYAN, '  video >> ')+locs['video'],
		color(DARK_CYAN, '  audio >> ')+locs['audio'],
		f'to change, edit {filename} or delete it and rerun script.')
	os.chdir(prv_dir)
	return locs

# set filename containing save-folder paths
paths_file = 'ytdlp_paths.txt'

def main():
	if not yrc.report():
		print2(color(GREEN, 'found')+' all dependencies')
	else:
		yrc.main()
		input('press enter to quit')
		quit()
	locations = check_file_for_paths(paths_file)
	video_folder = Rf'{locations['video']}'
	audio_folder = Rf'{locations['audio']}'
	while True:
		query = input(color(YELLOW, '  [START] >> download video, audio or quit? [V/a/q] '))
		if query.lower() in ['q', 'quit', 'exit']:
			quit()
		elif query and str(query).lower() not in ['v', 'vid', 'video']:
			download_loop(audio_folder, 'audio')
		else:
			download_loop(video_folder, 'video')

if __name__ == '__main__':
	main()
