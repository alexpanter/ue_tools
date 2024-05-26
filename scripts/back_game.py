import datetime
import sys
import threading
import zipfile
from pathlib import Path

current_dir = Path.cwd()
game_dir = sys.argv[1]
print("current_dir: ", current_dir)
print("game_dir: ", game_dir)

def get_files(gameDir: Path):
    folders = ["Config", "Content", "Docs", "Platforms", "Source"]
    files_to_zip = []
    for folder in folders:
        files_to_zip.extend([(file, file.relative_to(gameDir)) for file in (gameDir/folder).rglob('*') if file.is_file()])

    files_to_zip.extend([
        (file, file.relative_to(gameDir)) for file in gameDir.glob('*') if file.is_file() and file.parent == gameDir
    ])

    return files_to_zip

files = get_files(current_dir/game_dir)
outname = game_dir + "-" + datetime.datetime.now().strftime("%Y%m%d-%H%M") + ".zip"
files_processed = 0
num_files = len(files)

def print_job():
    if files_processed >= num_files:
        return
    threading.Timer(2.0, print_job).start()
    print("Processed ", files_processed, " out of ", num_files, " files.")

print_job()

with zipfile.ZipFile(current_dir/outname, 'w', zipfile.ZIP_DEFLATED) as zip_f:
    for file, rel in files:
        zip_f.write(file, rel)
        files_processed += 1

print("Finished creating zip.")
