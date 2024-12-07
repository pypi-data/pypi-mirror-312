import logging
from yachalk import chalk

# Use the COLORS dictionary to store colors
class KnowledgeGraphLogger:
    COLORS = {
        "black": chalk.black,
        "red": chalk.red,
        "green": chalk.green,
        "yellow": chalk.yellow,
        "blue": chalk.blue,
        "magenta": chalk.magenta,
        "cyan": chalk.cyan,
        "white": chalk.white,
        "black_bright": chalk.black_bright,
        "red_bright": chalk.red_bright,
        "green_bright": chalk.green_bright,
        "yellow_bright": chalk.yellow_bright,
        "blue_bright": chalk.blue_bright,
        "magenta_bright": chalk.magenta_bright,
        "cyan_bright": chalk.cyan_bright,
        "white_bright": chalk.white_bright,
        "grey": chalk.grey,
    }

    def __init__(self, name="Graph Logger", color="white", level="INFO"):
        self._name = name
        self._color = color
        self._log_level = level
        self._logger = self._setup_logger()

    # Set and return the configured logger object
    def _setup_logger(self):
        logger = logging.getLogger(self._name)
        logger.setLevel(self._log_level)
        logger.propagate = False

        # Define the format of log information
        formatter = logging.Formatter(
            self._format_message(),
            datefmt=self._time_format()
        )

        # Output log information to the stream
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        
        # Add the configured processor to the logger object
        logger.addHandler(handler)
        
        return logger
    
    # Returns a formatted message template based on the selected color
    def _format_message(self):
        color_function = self.COLORS.get(self._color)
        return color_function(
            "\n▶︎ %(name)s - %(asctime)s - %(levelname)s \n%(message)s\n"
        )

    # return time format
    def _time_format(self):
        return "%Y-%m-%d %H:%M:%S"

    # Returns the configured logger object
    def getLogger(self):
        return self._logger

# Create a logger
def create_logger(name, color):
    return KnowledgeGraphLogger(name, color).getLogger()

# Initialize the logger
loggers = {
    "INFO": create_logger("KNOWLEDGE GRAPH BUILDER LOG", "green_bright"),
    "ERROR": create_logger("KNOWLEDGE GRAPH BUILDER ERROR", "red_bright"),
    "DEBUG": create_logger("KNOWLEDGE GRAPH BUILDER DEBUG", "blue_bright")
}