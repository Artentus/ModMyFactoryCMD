from enum import Enum

class Build(Enum):
    ALPHA = "alpha"
    DEMO = "demo"
    HEADLESS = "headless"

    @staticmethod
    def list():
        return list(map(lambda i: i.value, Build))

class Platform(Enum):
    WIN64 = "win64"
    WIN64_MANUAL = "win64-manual"
    WIN32 = "win32"
    WIN32_MANUAL = "win32-manual"
    OSX = "osx"
    LINUX64 = "linux64"
    LINUX32 = "linux32"

    @staticmethod
    def list():
        return list(map(lambda i: i.value, Platform))

class ApiError(Exception):
    message = ""
    def __init__(self, message):
        self.message = message

class AuthError(ApiError):
    def __init__(self):
        return super().__init__("Authentication failed.")

class ServerError(Exception):
    status_code = 0
    def __init__(self, status_code):
        self.status_code = status_code
        