from modules.load_env import EnvironmentVariables
from modules.email_reader import EmailReader
from modules.database import Database
from modules.code_service import CodeService

ENV = EnvironmentVariables()

def main() -> None:
  database_args = [ENV.REDIS_URL]
  email_reader_args = [ENV.MAIL_SERVER, ENV.EMAIL, ENV.PASSWORD]

  database = Database(*database_args)
  email_reader = EmailReader(*email_reader_args)

  code_service = CodeService(database, email_reader)
  code_service.run()

  database.close()  
  email_reader.logout()

if __name__ == "__main__":
  main()

