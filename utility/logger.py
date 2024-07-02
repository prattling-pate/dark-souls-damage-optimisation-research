from logic.file import File
from logic.commands import Append
from datetime import datetime

class Logger:
    def __init__(self, file_path : str):
        self._file = File(file_path)
    
    def log(self, to_log : str):
        now = datetime.now()
        now_str = now.strftime("%d/%m/%Y %H:%M:%S")
        message : str = f"<Info> {now_str} :" + to_log
        self._file.modify_contents(Append(), -1 , message)

    def write_log(self):
        self._file.write_to_file()
