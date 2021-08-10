from os import listdir, rename, mkdir, remove, stat
from os.path import isfile, join, isdir, splitext
from datetime import datetime

DOWNLOADS = "/Volumes/3d printing"

only_files = [f for f in listdir(DOWNLOADS) if isfile(join(DOWNLOADS, f))]
only_dirs = [d for d in listdir(DOWNLOADS) if isdir(join(DOWNLOADS, d))]
for file in only_files:
    name, extension = splitext(join(DOWNLOADS,file))
    directory = extension
    date = datetime.fromtimestamp(stat(join(DOWNLOADS, file)).st_ctime)
    if int(date.strftime("%Y")) >=  2020:     # only look at files from 2020 or newer
        if directory == "zip" or directory == "blend" or directory == "stl" or directory =="pdf" or directory == 'gcode' or \
                directory == "png" or directory == "jpeg" or directory == "jpg":
            if isdir(join(DOWNLOADS,directory)):   # the directory has been made for the download
                rename(join(DOWNLOADS, file), join(DOWNLOADS, directory, file))
            else:
                mkdir(join(DOWNLOADS, file.split(".")[-1]))    # make a directory with the extension and move it to there
                rename(join(DOWNLOADS, file), join(DOWNLOADS, file.split(".")[-1], file))
        elif directory == "dmg" or directory == 'pkg' or directory == 'exe' or directory == '3mf':   #delete the installer packages
            remove(join(DOWNLOADS, file))
    else:    #  Delete older files
        remove(join(DOWNLOADS, file))

# ## Create backup folder ## #
backup_folder = datetime.now().strftime("backup-%d-%m-%Y")
try:
    mkdir(join(DOWNLOADS,backup_folder))
except FileExistsError:
    print("Folder exists")
for dir in only_dirs:    # Move folders into a backup folder
    if 'backup' != dir.split("-")[0]:  # move folders to back-up folder
        try:
            rename(join(DOWNLOADS,dir),join(DOWNLOADS,backup_folder,dir))
        except PermissionError:
            print("Permission Error:  System or Hidden Folder")
