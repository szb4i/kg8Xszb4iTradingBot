# ESSENTIAL!! every action should be logged with timestamp in a consistent way - e.g. TIMESTAMP | ACTION | PARAMS
import logging
import datetime

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
        # TODO
        # datum szerinti particionalas. file name: aznapi datum
        # historikus logokat szerverrol leszedni, hogy ne teljen meg a memoria
        file_name = datetime.datetime.now().strftime('%Y-%m-%d') + '.log'
        logging.basicConfig(filename=file_name, encoding='utf-8', level=logging.DEBUG, format='%(asctime)s.%(msecs)03d | %(message)s', datefmt='%Y.%m.%d %H:%M:%S')
        self.info('kg8Xszb4iTradingBot started running')

    def info(self, message):
        self.logger.info(message)
