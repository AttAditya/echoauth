from imaplib import IMAP4_SSL
from email import message_from_bytes
from email.header import decode_header
from datetime import datetime

class Mail:
  _mail_server: IMAP4_SSL
  _mail_id: str

  sender: str
  subject: str
  body: str
  date: str

  def __init__(self, mail_server: IMAP4_SSL, mail_id: str):
    self._mail_server = mail_server
    self._mail_id = mail_id
    
    self.load()

  def load(self) -> None:
    mail_server = self._mail_server
    mail_id = self._mail_id

    _, mail_data = mail_server.fetch(mail_id, "(RFC822)")
    
    if not mail_data: raise ValueError()
    if not mail_data[0]: raise ValueError()

    raw_email = mail_data[0][1]
    message = message_from_bytes(raw_email) # type: ignore

    self.sender = message["From"]
    self.date = message["Date"]
    
    self.body = self.get_email_body(message)
    
    self.subject, encoding = decode_header(message["Subject"])[0]
    if isinstance(self.subject, bytes):
      self.subject = self.subject.decode(
        encoding if encoding else "utf-8"
      )

  def get_epoch(self) -> int:
    DEFAULT_FORMAT = "%a, %d %b %Y %H:%M:%S %z"
    dt = datetime.strptime(self.date, DEFAULT_FORMAT)
    return int(dt.timestamp())
  
  def get_email_body(self, msg) -> str:
    if not msg.is_multipart():
      return msg.get_payload(decode=True).decode(errors="ignore")
  
    for part in msg.walk():
      if part.get_content_type() != "text/plain": continue
      if part.get_content_disposition() is not None: continue
      
      return part.get_payload(decode=True).decode(errors="ignore")
    
    return ""
  
  def mark_read(self) -> None:
    self._mail_server.store(
      self._mail_id, "+FLAGS", "\\Seen"
    )

  def get_email_id(self) -> str:
    email = self.sender[:-1].split("<")[-1]
    return email

