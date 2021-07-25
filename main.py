#  python -m pip install pysimplegui extract_msg tinydb
import extract_msg
import PySimpleGUI as sg
import os.path
from time import time
from tinydb import TinyDB, Query
from gui import window
from settings import get_settings, set_settings


SETTINGS_FILE = 'settings.json'


def meet_criteria(msg, options):
    [sender, to, cc, keywords,
     to_and_cc, attachments, subject_only] = options
    if len(sender) > 0:
        if sender not in msg['Sender']:
            return False
    if to_and_cc:
        searchlist = to + cc
        if len(searchlist) > 0:
            if not any([key in msg['To'] or key in msg['CC'] for key in searchlist]):
                return False
    else:
        if len(to) > 0:
            if not any([key in msg['To'] for key in to]):
                return False
        if len(cc) > 0:
            if not any([key in msg['CC'] for key in cc]):
                return False
    if attachments:
        if msg['Attachments'] == 0:
            return False
    else:
        if msg['Attachments'] > 0:
            return False
    if len(keywords) > 0:
        if subject_only:
            if not any([key in msg['Subject'] for key in keywords]):
                return False
        else:
            if not any([key in msg['Subject'] or key in msg['Body'] for key in keywords]):
                return False

    return True


def show_meter_but_cancelled(i, n, msg, title='Search in Progress'):
    res = sg.one_line_progress_meter(
        title, i, n,  msg)
    return i < n and not res


def search(db, options, preview_options):
    res = []
    for f in db:
        try:
            if meet_criteria(f, options):
                res.append(f['Filename'])
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


def update_filenames(folder):
    try:
        # Get list of files in folder
        file_list = os.listdir(folder)
    except:
        file_list = []
    return [
        f
        for f in file_list
        if os.path.isfile(os.path.join(folder, f))
        and f.lower().endswith((".msg"))
    ]


def main():
    fnames = []
    inbox, outbox = get_settings(SETTINGS_FILE)
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        # Folder name was filled in, make a list of files in the folder
        if event == "-FOLDER-":
            folder = values["-FOLDER-"]
            fnames = update_filenames(folder)
        elif event == "-GO-":
            if len(fnames) == 0:
                sg.popup("Please select a folder with msg files.")
            else:
                sender = values["-SENDER-"].lower()
                to = values["-TO-"].replace(";", ",").lower().split(",")
                cc = values["-CC-"].replace(";", ",").lower().split(",")
                keywords = values[
                    "-KEYWORDS-"].replace(";", ",").replace(" ", ",").lower().split(",")
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
                    ###########################################################
                    # update database
                    # recorded = TinyDB(os.path.join(folder, 'recorded.json'))
                    tinydb = TinyDB(os.path.join(folder, 'db.json'))
                    # mails = Query()
                    recorded = tinydb.table('recorded')
                    db = tinydb.table('db')
                    cancelled = False
                    filenames = set()
                    for filename in recorded:
                        filenames.add(filename['Filename'])
                    step_time = time()
                    for i in range(len(fnames)):
                        # if i % 100 == 0:
                        if time() - step_time > 0.5:
                            step_time = time()
                            if show_meter_but_cancelled(i + 1, len(fnames), "Update Database...\n\n", title="Update Database"):
                                cancelled = True
                                break
                        file = fnames[i]
                        # if len(recorded.search(mails.Filename == file)) == 0:
                        if file not in filenames:
                            msg = extract_msg.Message(
                                os.path.join(folder, file))
                            recorded.insert({'Filename': file})
                            db.insert({
                                'Sender': str(msg.sender).lower(),
                                'Filename': file,
                                'To': str(msg.to).lower(),
                                'CC': str(msg.cc).lower(),
                                'Subject': str(msg.subject).lower(),
                                'Body': str(msg.body)[:500].lower(),
                                'Attachments': len(msg.attachments)
                            })
                    show_meter_but_cancelled(100, 100, "")
                    ###########################################################
                    # Search
                    if not cancelled:
                        hit_list = search(db, [sender, to, cc, keywords,
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
                # print(preview(filename))
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
        elif event == "-INBOX-":
            if len(inbox) > 0:
                window["-FOLDER-"].update(inbox)
                folder = inbox
                fnames = update_filenames(inbox)
        elif event == "-OUTBOX-":
            if len(outbox) > 0:
                window["-FOLDER-"].update(outbox)
                folder = outbox
                fnames = update_filenames(outbox)
        elif event == "-SETTINGS-":
            set_settings(SETTINGS_FILE)
            inbox, outbox = get_settings(SETTINGS_FILE)

    window.close()

if __name__ == "__main__":
    main()
