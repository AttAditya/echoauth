from os import environ
from os.path import exists

class EnvironmentVariables:
  MAIL_SERVER: str
  EMAIL: str
  PASSWORD: str

  REDIS_URL: str

  def __init__(self) -> None:
    self.load_env()
    self.initialize()

  def initialize(self) -> None:
    self.MAIL_SERVER = environ.get("MAIL_SERVER", "")
    self.EMAIL = environ.get("EMAIL", "")
    self.PASSWORD = environ.get("PASSWORD", "")
    self.REDIS_URL = environ.get("REDIS_URL", "")

  def load_env(self) -> None:
    if not exists(".env"):
      return

    with open(".env") as env_file:
      for line in env_file.readlines():
        key, value = line.strip().split("=", 1)
        environ[key] = eval(value)

