import PySimpleGUI as sg
from tinydb import TinyDB, Query


def get_settings(filename):
    settings = TinyDB(filename)
    try:
        folders = Query()
        inbox = settings.search(folders.type == "inbox")[0]['dir']
        outbox = settings.search(folders.type == "outbox")[0]['dir']
    except:
        inbox = ''
        outbox = ''
    return inbox, outbox


def set_settings(filename):
    inbox, outbox = get_settings(filename)
    layout = [
        [
            sg.Text("Inbox Default", size=(15, 1)),
            sg.In(inbox, size=(60, 1), enable_events=True, key="-INBOX-"),
            sg.FolderBrowse()
        ],
        [
            sg.Text("Outbox Default", size=(15, 1)),
            sg.In(outbox, size=(60, 1), enable_events=True, key="-OUTBOX-"),
            sg.FolderBrowse()
        ],
        [
            sg.OK(), sg.Cancel()
        ]
    ]
    window = sg.Window("Settings", layout)
    while True:
        event, values = window.read()
        if event == "Cancel" or event == sg.WIN_CLOSED:
            break
        if event == "OK":
            inbox = values['-INBOX-']
            outbox = values['-OUTBOX-']
            try:
                settings = TinyDB(filename)
                settings.truncate()
                settings.insert({'type': 'inbox', 'dir': inbox})
                settings.insert({'type': 'outbox', 'dir': outbox})
            except:
                pass
            break

    window.close()
