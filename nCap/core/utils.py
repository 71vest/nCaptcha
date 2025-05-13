from core.imports import random, string

class utility:
    def __init__(self) -> None:
        pass

    def createId(self, len: int):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=len))