import logging
from logging.handlers import RotatingFileHandler
from colorama import Fore, Style
import datetime


class InetCentralHandler(logging.Handler):
    """
    Handler for sending logs to InetCentral
    inet_handler = InetCentralHandler("http://localhost:3000", "parser_logs")
    """
    def __init__(self, host, index_name):
        super().__init__()
        self.inetCentral = InetCentral([host])
        self.index_name = index_name
    def emit(self, record):
        try:
            #formater
            log_entry = {
                'timestamp': datetime.utcnow(),
                'level': record.levelname,
                'message': record.getMessage(),
                'module': record.module,
                'function': record.funcName,
                'line': record.lineno,
                'trace': None
            }

            #add stacktrace
            if record.exc_info:
                log_entry['trace'] = self.formatter.formatException(
                    record.exc_info)

            #send to central
            self.es.index(index=self.index_name, document=log_entry)
        except Exception as e:
            print(f"Error sending log to InetCentral: {e}")

class ColoredFormatter(logging.Formatter):
    """Добавляем настройки цвета сообщений"""
    COLORS = {
        logging.DEBUG: Fore.BLUE,
        logging.INFO: Fore.GREEN,    
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT
    }

    def format(self, record):
        if record.levelno in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelno]}{record.levelname}{Style.RESET_ALL}"
            record.asctime = f"{self.COLORS[record.levelno]}{record.created}{Style.RESET_ALL}"
            record.msg = f"{self.COLORS[record.levelno]}{record.msg}{Style.RESET_ALL}"
            record.filename = f"{self.COLORS[record.levelno]}{record.filename}{Style.RESET_ALL}"
            record.funcName = f"{self.COLORS[record.levelno]}{record.funcName}{Style.RESET_ALL}"
        return super().format(record)


class BasicLog:
    def __init__(self, log_file_path: str, stream: bool = True) -> None:
        self.log_file_path = log_file_path
        self.stream = stream

    def log_config(
            self, 
            name:str, 
            loglevel= logging.DEBUG
            ) -> logging.Logger:
        """
        Configuration of the logger.

        Args:
            name (str): The name of the logger.
            stream (bool, optional): Whether to log to a stream or a file. Defaults to True.
            loglevel (int, optional): The level of the messages to log. Defaults to logging.DEBUG.

        Returns:
            logging.Logger: The configured logger.
        """
        logger_name = (name)
        logger = logging.getLogger(logger_name)
        logger.setLevel(loglevel)
        formater = ColoredFormatter('%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s')
        conf = {
            True: self.stream_conf(formater),
            False: self.file_conf(formater)
        }
        #добавление хендлера
        logger.addHandler(conf[self.stream])
        return logger

    def stream_conf(self, formater):
        #настройки для консоли
        stream = logging.StreamHandler()
        stream.setFormatter(formater)
        return stream
    
    def file_conf(self, formater):
        #настройки для лог-файла
        log_file = RotatingFileHandler(self.log_file_path, maxBytes=100000, backupCount=3)
        log_file.setFormatter(formater)
        return log_file
