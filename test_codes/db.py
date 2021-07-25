#  python -m pip install pysimplegui extract_msg
import extract_msg
import os.path
from tinydb import TinyDB, Query


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

folder = r"../msg"
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
recorded = TinyDB('recorded.json')
db = TinyDB('db.json')
mails = Query()

for file in fnames:
    if len(recorded.search(mails.Filename == file)) == 0:
        msg = extract_msg.Message(os.path.join(folder, file))
        recorded.insert({'Filename': file})
        db.insert({
            'Sender': str(msg.sender).lower(),
            'Filename': file,
            'To': str(msg.to).lower(),
            'CC': str(msg.cc).lower(),
            'Subject': str(msg.subject).lower(),
            'Body': str(msg.body)[:500].lower()
        })
