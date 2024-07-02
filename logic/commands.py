from typing import Callable

def _delete(line : str, index : int) -> str:
    newline = line[0:index] + line[index+1:]
    return newline

def _change(line : str, index : int, newchar : str):
    newline = line[0:index] + newchar + line[index+1:]
    return newline

def _insert(line: str, index : int, newchar : str):
    newline = line[0:index] + newchar + line[index:]
    return newline

def _append(line: str, newchar : str):
    newline = line + "\n" + newchar
    return newline

def _new_line(line : str):
    newline = line + "\n"
    return newline


class Command:
    """Class representing a text editing command"""
    def __init__(self, fn : Callable):
        self._command_function : Callable = fn

    def execute_command(self, *args) -> str:
        return self._command_function(*args)
    
class Delete(Command):
    def __init__(self):
        super().__init__(_delete)

class Change(Command):
    def __init__(self):
        super().__init__(_change)

class Insert(Command):
    def __init__(self):
        super().__init__(_insert)

class Append(Command):
    def __init__(self):
        super().__init__(_append)

class NewLine(Command):
    def __init__(self):
        super().__init__(_new_line)
