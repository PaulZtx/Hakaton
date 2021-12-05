# image_viewer.py
import threading
import zipfile
from main import start
import io
import os
import PySimpleGUI as sg
from threading import Thread
from PIL import Image

sg.theme('Light Blue 2')
file_types = [("JPEG files (*.jpg)", "*.jpg"),
              ("PNG files (*.png)", "*.png"),
              ("ZIP files (*.zip)", "*.zip")]


def run_from_folder(name):
    # directory = name
    # files = os.listdir(directory)
    # images = filter(lambda x: x.endswith('.jpg') or x.endswith('.png'), files)
    thread = Thread(target=start, args=(name,))
    thread.daemon = True
    thread.name = "AI"
    thread.start()
    #sg.popup([i for i in images])

def run_from_file(name):
    lower_name = name[-3:].lower()
    if lower_name in ("png", "jpg"):
        path = os.getcwd()

        n = name.split('/')
        #sg.popup(n[-1])
        if not os.path.isdir("Animals"):
            os.mkdir("Animals")
        new_name = "Animals/" + n[-1]
        os.replace(name, new_name)
        run_from_folder("Animals")

    if lower_name == "zip":
        animal_zip = zipfile.ZipFile(name)
        animal_zip.extractall("Animals")
        run_from_folder("Animals")

def check_files():
    pass

def main():
    toggle_disabled = False
    global thread
    layout = [
        [sg.Image(key="-IMAGE-")],
        [
            [sg.Text("Выбор папки "), sg.Input(size=(25, 1), key="-FILEFOLDER-"), sg.FolderBrowse(key="-OpenFolder-")],
            [sg.Text("Выбор файла"), sg.Input(size=(25, 1), key="-FILE-"), sg.FileBrowse(file_types=file_types, key="-OpenFile-")],
            sg.Button("Загрузить файл", bind_return_key=True, disabled=toggle_disabled),
        ],
    ]

    window = sg.Window("Geekata", layout)


    while True:
        event, values = window.read()

        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        if "AI" in [t.name for t in threading.enumerate()]:
            window["Загрузить файл"].update(disabled=False)
            sg.popup("Yes")

        if event == "Загрузить файл":

            if values["-FILEFOLDER-"] == "" and values["-FILE-"] == "":
                sg.popup("Файл не выбран!")

            elif values["-FILEFOLDER-"] != "":
                run_from_folder(values["-FILEFOLDER-"])
                toggle_disabled = True
                window["Загрузить файл"].update(disabled=toggle_disabled)
                #sg.popup("AI" in [t.name for t in threading.enumerate()])

            elif values["-FILE-"] != "":
                filename = values["-FILE-"]
                if filename[-3:] not in ("png", "jpg", "rar", "zip", "PNG", "JPG", "RAR", "ZIP"):
                    sg.popup("Неверный ввод, повторите попытку")

                else:
                    toggle_disabled = True
                    window["Загрузить файл"].update(disabled=toggle_disabled)
                    run_from_file(values["-FILE-"])




    window.close()


if __name__ == "__main__":
    main()