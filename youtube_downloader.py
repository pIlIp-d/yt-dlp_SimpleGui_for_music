import PySimpleGUI as sg
from subprocess import check_call, CalledProcessError
import os
import threading

YT_DL_PATH = os.path.join(os.path.dirname(__file__), "yt-dlp")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "music")
OUTPUT_DIR_FILE_PATH = os.path.join(OUTPUT_DIR, "%(title)s.%(ext)s")

def downloadPlaylist(window, url: str, ignore_errors: bool):
    options = [
        YT_DL_PATH, "-x", "--audio-format", "mp3", "--audio-quality", "0", "--embed-thumbnail",
        "--add-metadata", "--output", OUTPUT_DIR_FILE_PATH, url
    ]
    if ignore_errors:
        options.append("--ignore-errors")
    try:
        check_call(options)
    except CalledProcessError:
        window["error_msg"].update("Es gab einen Fehler")
    window["status"].update("finished")

def cleanup_folder():
    for file in os.listdir(OUTPUT_DIR):
        if file.endswith("webp") or file.endswith("webm") or file.endswith("part"):
            os.remove(os.path.join(OUTPUT_DIR, file))

if __name__ == "__main__":
    layout = [
                [sg.Text('Video oder Playlist URL'), sg.InputText(key='url')],
                [sg.Checkbox('ignore errors', default=False, key='ignore_errors'), sg.Button('Download'), sg.Text('', key='status'), sg.Text('', key='error_msg', text_color="red")]
             ]
    window = sg.Window('Youtube Downloader', layout)
    while True:
        event, values = window.read()
        window["error_msg"].update("")
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Download':
            window["status"].update("downloading...")
            window.refresh()
            def run():
                downloadPlaylist(window, values["url"], values["ignore_errors"])
            threading.Thread(target=run, daemon=True).start()

    window.close()
    cleanup_folder()
