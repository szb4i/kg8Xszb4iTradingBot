# ESSENTIAL!! every action should be logged with timestamp in a consistent way - e.g. TIMESTAMP | ACTION | PARAMS
import logging

class Logger:
    _instance = None
    
    def __init__(self) -> None:
        raise RuntimeError('Logger needs to be used as a singleton. Call get_singleton() instead!')
    
    @classmethod
    def get_singleton(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls.__init_singleton(cls)
        return cls._instance
    
    def __init_singleton(self):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(filename='logger/logs/logs.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s.%(msecs)03d | %(message)s', datefmt='%Y.%m.%d %H:%M:%S')

    def info(self, message):
        self.logger.info(message)
