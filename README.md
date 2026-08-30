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
  - with pip get python lib, linux might need to enter a venv to install with pip, ubuntu does atleast, see ubuntu section below on how to:
    - yt-dlp -> ```pip install yt-dlp``` -> https://pypi.org/project/yt-dlp/
    - yt-dlp-ejs -> ```pip install yt-dlp-ejs``` ->https://pypi.org/project/yt-dlp-ejs/
    - mutagen -> ```pip install mutagen``` -> https://pypi.org/project/mutagen/

### ubuntu (26.04), probably any instance where venv is required and/or wanted
- virtual env (venv) is needed to install pkgs with pip, so do:
  1. make sure pip and venv is installed:
     - ```sudo apt update```
     - ```sudo apt install -y python3-pip python3-venv```
  2. then navigate to your ```yt-dlp.py``` folder in your terminal and:
     1. ```python3 -m venv venv```
     2. ```source venv/bin/activate```
     3. ```python3 -m pip install yt-dlp yt-dlp-ejs mutagen```
  3. test if all ok with:
     - ```python3 ytdlp_req_check.py```
  4. lastly exit venv as you have no need to be there anymore.
     - ```deactivate```
  5. set up an alias command to enter and exit venv when you need to run this script, see ytdlp.bat section.
  6. if yt-dlp or another module ever needs to be updated, then enter venv as per step 2.2, run the cmd below and lastly exit venv as per step 4:
     - ```python3 -m pip install yt-dlp --upgrade```


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
point of the file ```ytdlp.bat``` is to facilitate calling, in this case ```ytdlp```, in cmd from anywhere which will execute ```yt-dlp.py```.
to do so however the file location have to be added to environment variables and the file has to be edited to point to ```yt-dlp.py``` location.
1. place ```ytdlp.bat``` in eg. ```C:\tools``` or another created-by-you folder or alternatively, leave it in the same folder as the script above.
  2. rename it to ```your_name.bat```if you wish the command you use to be something else. the command will be == to the filename
3. edit file (with text editor) and replace ```path\to\yt-dlp.py``` with ```your path\yt-dlp.py```.
4. add the folder to ```path environment variables```
   - environment variables -> mark PATH in user if only for that user or system for everybody and hit edit -> hit New and enter the path to the bat file, eg. ```C:\tools```.

### for linux
the file ```ytdlp.bat``` is not needed for linux.  
instead, simply add the following to your bash profile, or whatever else shell, terminal whatever you run. if you run something else you can probably figure this out on your own np. if you did not need/want venv when installing with pip then:  
  ```echo "alias ytdlp='python3 /full/path/to/yt-dlp.py'" >> ~/.bashrc```  
else do for venv:  
  ```echo "alias ytdlp='cd path/to/yt-dlp.py && source venv/bin/activate && python3 yt-dlp.py && deactivate && cd $OLDPWD'```  
which adds a new line in .bashrc with the alias which when you call ytdlp will:  
- move terminal directory to your file
- activate an already created virtual environment named venv
- execute the script
- deactivate the venv when you quit the script
- lastly it returns the terminal to the previous working directory, wherever your terminal was before

then restart your terminal or do:  
  ```source ~/.bashrc```  
which should refresh the terminal with the new settings set in the file.  
you should now be able to call ```ytdlp``` (or whatever command you set instead) from your terminal and it will start the script.  

### other OS
not a damn clue

## using wrapper
- run it in your cmd/term whatever of choice with ```py yt-dlp.py``` or your ```ytdlp``` command if you set it up.
- it will ask whether a video or audio is wanted, eg you can choose audio and enter a link to video and still only receive an audio file as output
- paste link to whatever video or audio you wish to download.
- the wrapper will report the file(s) downloaded, the location they were saved and the size of file(s)
- the wrapper will check for duplicates in the destination folder selected and report findings.
  - if duplicate is found, the name of duplicate file gets appended a (n), eg if 3 identically named files already exits and a 4th is downloaded, then:
    - ```this_video_is_fantastic (4).png```
- once downloaded it will go ask for a link again. this continues untill you close the wrapper.
- you can switch between video and audio without having to restart the wrapper, see the prompt displayed in cmd/term