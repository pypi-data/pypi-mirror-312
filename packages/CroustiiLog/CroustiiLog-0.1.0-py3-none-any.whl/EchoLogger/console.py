import time
from colorama import Fore, Style
from .utils import get_timestamp, is_valid_log_level

class CustomLog:
    def __init__(self, log_format="{timestamp} LEVEL > message", color_map=None, valid_levels=None):
        self.log_format = log_format
        self.color_map = color_map or {
            "INFO": "\x1b[38;5;141m",
            "DEBUG": Fore.YELLOW,
            "ERROR": Fore.RED,
            "FATAL": Fore.MAGENTA,
            "SUCCESS": "\x1b[38;5;218m"
        }
        self.valid_levels = valid_levels or ["INFO", "DEBUG", "ERROR", "FATAL", "SUCCESS"]

    def log(self, message, *args, **kwargs):
        """Log a custom message with additional key-value information."""
        timestamp = get_timestamp()  # Get current timestamp
        grey_timestamp = f"{Fore.LIGHTBLACK_EX}{timestamp}{Style.RESET_ALL}"  # Timestamp in grey
        
        # Base log message with the grey timestamp
        formatted_message = f"{grey_timestamp} {message}"

        # Format additional arguments (key-value pairs) with grey for keys and '='
        if kwargs:
            formatted_message += " " + " | ".join(f"{Fore.LIGHTBLACK_EX}{key}{Style.RESET_ALL}={Fore.LIGHTBLACK_EX}{value}{Style.RESET_ALL}" for key, value in kwargs.items())
        
        print(formatted_message)

    def log_message(self, level, message, *args, **kwargs):
        if not is_valid_log_level(level, self.valid_levels):
            raise ValueError(f"Invalid log level: {level}")
        
        timestamp = get_timestamp()  # Get the timestamp
        grey_timestamp = f"{Fore.LIGHTBLACK_EX}{timestamp}{Style.RESET_ALL}"  # Timestamp in grey
        level_color = self.color_map.get(level, Fore.WHITE)
        
        # Format the log message with the log level and timestamp
        formatted_message = self.log_format.replace("{timestamp}", grey_timestamp).replace("LEVEL", f"{level_color}{level}{Style.RESET_ALL}").replace("message", message)

        # Print the log message
        print(formatted_message.format(timestamp=timestamp, *args, **kwargs))

    def info(self, message, *args, **kwargs):
        self.log_message("INFO", message, *args, **kwargs)

    def debug(self, message, *args, **kwargs):
        self.log_message("DEBUG", message, *args, **kwargs)

    def error(self, message, *args, **kwargs):
        self.log_message("ERROR", message, *args, **kwargs)

    def fatal(self, message, *args, **kwargs):
        self.log_message("FATAL", message, *args, **kwargs)

    def success(self, message, *args, **kwargs):
        self.log_message("SUCCESS", message, *args, **kwargs)

class BetaConsole:
    def __init__(self, speed=1):
        self.speed = speed

    def getTimestamp(self):
        return time.strftime("%H:%M:%S", time.localtime())

    def alphaPrint(self, prefix, message, increment=True):
        timestamp = self.getTimestamp()
        full_message = f"[{timestamp}] {prefix} > {message}"
        for char in full_message:
            print(char, end="", flush=True)
            time.sleep(1 / self.speed)
        print()

def main():
    console = CustomLog()
    console.info("This is an info message")
    console.debug("This is a debug message")
    console.error("This is an error message")
    console.success("This is a success message")
    console.fatal("This is a fatal message")

    beta_console = BetaConsole(speed=5)
    beta_console.alphaPrint("[INFO]", "Alpha printing at a custom speed")