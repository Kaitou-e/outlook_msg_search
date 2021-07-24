import extract_msg
import os.path


def read_msg(filename, printing=False):
    msg = extract_msg.Message(filename)
    msg_sender = msg.sender
    msg_date = msg.date
    msg_subj = msg.subject
    msg_message = msg.body

    if not printing:
        return
    # print(dir(msg))
    print('Sender: {}'.format(msg_sender))
    print("To", msg.to, type(msg.to))
    print("CC", msg.cc)
    print('Sent On: {}'.format(msg_date))
    print('Subject: {}'.format(msg_subj))
    print('Attachments: {}'.format(msg.attachments))
    # print('Body: {}'.format(msg_message))

folder = r'./msg/'  # Replace with yours
file_list = os.listdir(folder)
# print(file_list)
for filename in file_list:
    read_msg(folder + filename, printing=True)
