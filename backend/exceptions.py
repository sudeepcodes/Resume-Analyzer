import traceback


class GroqException(Exception):
    def __init__(self, message: str = "", *args):
        super().__init__(message, *args)
        self.traceback_info = traceback.format_exc()

    def __str__(self):
        return f"{self.args[0]} \nTraceback: {self.traceback_info}" if self.traceback_info else self.args[0]

