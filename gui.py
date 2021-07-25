import PySimpleGUI as sg

file_list_column = [
    [
        sg.Button("Folder Settings", key='-SETTINGS-'),
        sg.Button("Default Inbox", key='-INBOX-'),
        sg.Button("Default Outbox", key='-OUTBOX-')
    ],
    [
        sg.Text("Folder", justification="right", size=(8, 1)),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ], [sg.HorizontalSeparator()],
    [
        sg.Text("Sender", justification="right", size=(8, 1)),
        sg.In(size=(25, 1), enable_events=False, key="-SENDER-")
    ],
    [
        sg.Text("TO", justification="right", size=(8, 1)),
        sg.In(size=(25, 1), enable_events=False, key="-TO-")
    ],
    [
        sg.Text("CC", justification="right", size=(8, 1)),
        sg.In(size=(25, 1), enable_events=False, key="-CC-"),
        # sg.Button("Search", key="-GO-")
    ],
    [
        sg.Text("Keywords", justification="right", size=(8, 1)),
        sg.In(size=(25, 1), enable_events=False, key="-KEYWORDS-")
    ],
    [sg.Checkbox('Combine TO and CC', default=True, enable_events=False, key="-COMBINE-"),
     sg.Checkbox('Has Attachments', default=False, enable_events=False, key="-ATTACHMENTS-")],
    [sg.Checkbox('Search Keywords in Subject Only', enable_events=False,
                 default=True, key="-SUBJECT-KEYWORDS-ONLY-"),
     sg.Button("Search", key="-GO-", enable_events=True)
     ], [sg.HorizontalSeparator()],
    [sg.Text("Search Results")],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 17), key="-FILE LIST-"
        )
    ],
]
# For now will only show the name of the file that was chosen
image_viewer_column = [
    [sg.Text("Preview")],
    [sg.Multiline('', size=(45, 35), key="-PREVIEW-", enable_events=False)],
    [sg.Text(" ", size=(40, 1), key="-STATUS-", enable_events=False),
     sg.Button('Open', key="-OPEN-", enable_events=True)]
]
# ----- Full layout -----
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]
# To add the layout to your window, you can do this:
window = sg.Window("MSG Search", layout)
