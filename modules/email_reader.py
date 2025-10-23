from imaplib import IMAP4_SSL
from modules.mail import Mail

class EmailReader:
  def __init__(self, mail_server, email, password) -> None:
    self.mail = IMAP4_SSL(mail_server)
    self.mail.login(email, password)

  def fetch_unread(self) -> list[Mail]:
    self.mail.select("inbox", readonly=False)
    _, mails = self.mail.search(None, "UNSEEN")

    mail_ids = mails[0].split()
    mails = [
      Mail(self.mail, mail_id)
      for mail_id in mail_ids
    ]

    mails.sort(key=lambda mail: mail.get_epoch())

    return mails

  def logout(self) -> None:
    self.mail.logout()

