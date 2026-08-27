# yt-dlp wrapper script
### install:
- download:
  - python -> https://www.python.org/downloads/
  - deno -> https://deno.com/
  - ffmpeg, ffprobe -> https://www.ffmpeg.org/download.html
- place yt-dlp.py, ytdlp_req_check.py, ffmpeg, ffprobe in the same folder
- with pip get python lib:
  - yt-dlp -> pip install yt-dlp
    - https://pypi.org/project/yt-dlp/
  - yt-dlp-ejs -> pip install yt-dlp-ejs
    - https://pypi.org/project/yt-dlp-ejs/
  - mutagen -> pip install mutagen
    - https://pypi.org/project/mutagen/

**important to note, this script uses the python lib yt-dlp and not the standalone executable.**

when the script is run for the first time it will ask for locations to save downloaded video and audio files which is stored in a file it creates in the same directory as the script.
to change the paths, edit the file ```ytdlp_paths.txt``` or delete it and rerun script.

the script works with below stated versions:
- [exe] python 3.14.6
- [exe] deno 2.9.4
- [exe] ffmpeg 2026-07-30-git-2ae2413488-full_build-www.gyan.dev
- [exe] ffprobe 2026-07-30-git-2ae2413488-full_build-www.gyan.dev
- [lib] yt-dlp 2026.7.4
- [lib] yt-dlp-ejs 0.8.0
- [lib] mutagen 1.48.1-py3

### alias with ytdlp.bat
*for win10, lookup how to on another platform*
1. place ```ytdlp.bat``` in eg. ```C:\tools``` or another created-by-you folder or alternately, place it in the same folder as the script above.
2. add the folder to **path environment variables**
   - environment variables -> mark PATH and hit edit -> hit New and enter the path to the bat file, eg. ```C:\tools```.