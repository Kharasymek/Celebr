import datetime

class ErrorLogger:
    def __init__(self, filename="log.txt"):
        self.filename = filename

    def log_error(self, error_message):
        timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        with open(self.filename, "a") as file:
            file.write(f"{timestamp} {error_message}\n")