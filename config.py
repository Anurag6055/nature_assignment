import string

class Settings:
    DATABSE_URL = "sqlite:///./shortener.db"
    CODE_CHARACTERS = string.ascii_letters + string.digits
    CODE_LENGTH = 6

settings = Settings()