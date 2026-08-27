# yt-dlp wrapper script

### works on:
- windows 10 Version 22h2 (19045.6466)
- ubuntu 26.04 - virtualbox, linux should in general work
### install:
- do: ```git clone https://codeberg.org/lazukakabra/ytdlp.git``` where you wish the files to be or ```download as zip``` and extract where you wish the files to be, then >>
  - download,  linux can probably get from distro pkg mgr:
    - python -> https://www.python.org/downloads/
    - deno -> https://deno.com/
    - ffmpeg, ffprobe -> https://www.ffmpeg.org/download.html
      - ensure ffmpeg and ffprobe are in the same folder
        - for windows, add their location to PATH environment variable, see section ytdlp.bat below on how to add variable
  - with pip get python lib:
    - yt-dlp -> ```pip install yt-dlp``` -> https://pypi.org/project/yt-dlp/
    - yt-dlp-ejs -> ```pip install yt-dlp-ejs``` ->https://pypi.org/project/yt-dlp-ejs/
    - mutagen -> ```pip install mutagen``` -> https://pypi.org/project/mutagen/

**important to note, this script uses the python lib yt-dlp and not the standalone executable.**

when the script is run for the first time it will ask for locations to save downloaded video and audio files which is stored in a file it creates in the same directory as the script.
to change the paths, edit the file ```ytdlp_paths.txt``` or delete it and rerun script.

the script works with below stated versions, I have checked no other versions:
- [exe] python 3.14.6
- [exe] deno 2.9.4
- [exe] ffmpeg 2026-07-30-git-2ae2413488-full_build-www.gyan.dev
- [exe] ffprobe 2026-07-30-git-2ae2413488-full_build-www.gyan.dev
- [lib] yt-dlp 2026.7.4
- [lib] yt-dlp-ejs 0.8.0
- [lib] mutagen 1.48.1-py3

## ytdlp.bat - calling script with specific user set command/alias
### for win10
point of the file is to facilitate called, in this case ```ytdlp```, in cmd from anywhere which will execute ```yt-dlp.py```.
to do so however the files location have to be added to environment variables and the file has to be edited to point to ```yt-dlp.py``` location.
1. place ```ytdlp.bat``` in eg. ```C:\tools``` or another created-by-you folder or alternatively, leave it in the same folder as the script above.
2. edit file (with text editor) and replace ```path\to\yt-dlp.py``` with ```your path\yt-dlp.py```.
3. add the folder to ```path environment variables```
   - environment variables -> mark PATH in user if only for that user or system for everybody and hit edit -> hit New and enter the path to the bat file, eg. ```C:\tools```.

### for linux
simply add the following to your bash profile, or whatever else shell, terminal whatever you run. if you run something else you can probably figure this out on your own np:  
  ```echo alias ytdlp="python3 /full/path/to/yt-dlp.py" >> ~/.bashrc```  
which adds a new line in .bashrc with the alias. then restart your terminal or do:  
  ```source ~./bashrc```  
which should refresh the terminal with the new settings set in the file.  
you should now be able to call ```ytdlp``` (or whatever command you set instead) from your terminal and it will start the script.  

### other OS
not a damn clue