#  python -m pip install pysimplegui extract_msg
import extract_msg
import PySimpleGUI as sg
import os.path


def meet_criteria(msg, options):
    [sender, to, cc, keywords,
     to_and_cc, attachments, subject_only] = options
    if len(sender) > 0:
        if sender not in msg.sender:
            return False
    if to_and_cc:
        searchlist = to + cc
        if len(searchlist) > 0:
            if not any([key in msg.to or key in msg.cc for key in searchlist]):
                return False
    else:
        if len(to) > 0:
            if not any([key in msg.to for key in to]):
                return False
        if len(cc) > 0:
            if not any([key in msg.cc for key in cc]):
                return False
    if attachments:
        if len(msg.attachments) == 0:
            return False
    else:
        if len(msg.attachments) > 0:
            return False
    if len(keywords) > 0:
        if subject_only:
            if not any([key in msg.subject for key in keywords]):
                return False
        else:
            if not any([key in msg.subject or key in msg.body for key in keywords]):
                return False

    return True


def show_meter_but_cancelled(i, n, msg):
    res = sg.one_line_progress_meter(
        'Search in Progress', i, n,  msg)
    return i < n and not res


def search(folder, fnames, options, preview_options):
    res = []
    for i in range(len(fnames)):
        if show_meter_but_cancelled(
                i + 1, len(fnames),  preview_options + "\n" + "Found " + str(len(res)) + "\n\n"):
            break
        f = fnames[i]
        try:
            msg = extract_msg.Message(os.path.join(folder, f))
            if meet_criteria(msg, options):
                res.append(f)
        except:
            pass
    return res


def preview(filename):
    try:
        msg = extract_msg.Message(filename)
    except:
        print("open failed")
        return "Msg open error."
    res = "Sender: " + str(msg.sender) + "\n"
    res += "To: \n" + str(msg.to) + "\n"
    res += "CC: \n" + str(msg.cc) + "\n"
    res += "Sent On: " + str(msg.date) + "\n"
    res += "Subject: " + str(msg.subject) + "\n"
    res += "Attachments: " + str(msg.attachments) + "\n" + "\n"
    res += msg.body[:1000] + "\n"
    return res

file_list_column = [
    [
        sg.Text("Folder", justification="right", size=(8, 1)),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
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
        sg.In(size=(25, 1), enable_events=False, key="-KEYWORDS-"),
        sg.Button("Search", key="-GO-", enable_events=True)
    ],
    [sg.Checkbox('Combine TO and CC', default=True, enable_events=False, key="-COMBINE-"),
     sg.Checkbox('Has Attachments', default=False, enable_events=False, key="-ATTACHMENTS-")],
    [sg.Checkbox('Search Keywords in Subject Only', enable_events=False,
                 default=True, key="-SUBJECT-KEYWORDS-ONLY-")
     ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 18), key="-FILE LIST-"
        )
    ],
]
# For now will only show the name of the file that was chosen
image_viewer_column = [
    [sg.Text("Preview")],
    [sg.Multiline('', size=(45, 30), key="-PREVIEW-", enable_events=False)],
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
fnames = []
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Folder name was filled in, make a list of files in the folder
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []
        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".msg"))
        ]
        # window["-FILE LIST-"].update(fnames)
    elif event == "-GO-":
        if len(fnames) == 0:
            sg.popup("Please select a folder with msg files.")
        else:
            sender = values["-SENDER-"]
            to = values["-TO-"].replace(";", ",").split(",")
            cc = values["-CC-"].replace(";", ",").split(",")
            keywords = values[
                "-KEYWORDS-"].replace(";", ",").replace(" ", ",").split(",")
            to = [_ for _ in to if len(_) > 0]
            cc = [_ for _ in cc if len(_) > 0]
            keywords = [_ for _ in keywords if len(_) > 0]
            print(sender, to, cc, keywords)
            if len(sender) + len(cc) + len(keywords) + len(to) > 0:
                to_and_cc = values["-COMBINE-"]
                attachments = values["-ATTACHMENTS-"]
                subject_only = values["-SUBJECT-KEYWORDS-ONLY-"]
                # window["-PREVIEW-"].update(
                preview_options = "Search\nSender: %s\nTo: %s\nCC: %s\nKeywords: %s\n" % (
                    sender, ", ".join(to), ", ".join(cc), ", ".join(keywords)) + \
                    "Combine To and CC: %s\nHas attachments: %s\nSearch keywords in subject only: %s\n" % (
                        str(to_and_cc), str(attachments), str(subject_only)
                )
                # )
                hit_list = search(folder, fnames, [sender, to, cc, keywords,
                                                   to_and_cc, attachments, subject_only], preview_options)
                window["-FILE LIST-"].update(hit_list)
            else:
                sg.popup("Please set search conditions.")
    elif event == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            # window["-TOUT-"].update(filename)
            print("Preview", filename)
            print(preview(filename))
            window["-PREVIEW-"].update(preview(filename))
        except:
            pass
    elif event == "-OPEN-":
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            window["-PREVIEW-"].update("OPEN: %s" % filename)
        except:
            pass

window.close()
