#  python -m pip install pywin32
import win32com.client
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
msg = outlook.OpenSharedItem(r".\msg\2.msg")

print("Sender",msg.SenderName)
print("Sender email",msg.SenderEmailAddress)
print("Sent on",msg.SentOn)
print("To",msg.To)
print("CC",msg.CC)
print("BCC",msg.BCC)
print("Subject",msg.Subject)
print(msg.Body)

count_attachments = msg.Attachments.Count
if count_attachments > 0:
    for item in range(count_attachments):
        print(msg.Attachments.Item(item + 1).Filename)

del outlook, msg