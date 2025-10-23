from modules.database import Database
from modules.mail import Mail
from modules.email_reader import EmailReader

class CodeService:
  def __init__(self, database: Database, email_reader: EmailReader) -> None:
    self._database = database
    self._email_reader = email_reader

  def collect_emails(self) -> list[Mail]:
    mails = self._email_reader.fetch_unread()
    return mails

  def retrieve_code(self, mail: Mail) -> str:
    numbers = []

    for c in mail.body:
      if c.isdigit():
        numbers.append(c)

      if len(numbers) == 6:
        break
    
    code = "".join(numbers)
    return code

  def collect_codes(self, mails: list[Mail]) -> dict[str, str]:
    codes = {}

    for mail in mails:
      code = self.retrieve_code(mail)
      if not code: continue
      codes[mail.get_email_id()] = code

    return codes
  
  def save_codes(self, codes: dict[str, str]) -> None:
    self._database.save(codes)

  def run(self) -> None:
    mails = self.collect_emails()
    codes = self.collect_codes(mails)
    
    self.save_codes(codes)
    for mail in mails:
      mail.mark_read()

