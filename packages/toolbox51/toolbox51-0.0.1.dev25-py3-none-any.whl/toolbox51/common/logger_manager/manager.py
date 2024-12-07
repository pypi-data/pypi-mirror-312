


import asyncio
import logging
import time

from ..singleton import SingletonMeta
from ..logging import touch_logger


class LoggerManager(metaclass=SingletonMeta):
    
    default_level: int
    record: dict[str, float] = {}
    logger: logging.Logger
    secondary_logger: logging.Logger
    
    def __init__(self, default_level:int = logging.DEBUG) -> None:
        self.default_level = default_level
        self.logger = touch_logger("GLOBAL", level=self.default_level)
        self.secondary_logger = touch_logger("SECONDARY", level=self.default_level)
        
    def set_default_level(self, level: int) -> None:
        self.default_level = level
        self.logger.setLevel(level)
        self.secondary_logger.setLevel(level)

    def register(self, name:str) -> logging.Logger:
        self.record[name] = now_time = time.time()
        
        # 清除长期不用的logger
        to_delete = [k for k, v in self.record.items() if now_time - v > 600]
        for item in to_delete:
            self.unregister(item)
        
        return touch_logger(name, level=self.default_level)
        
    def unregister(self, name:str) -> None:
        self.record.pop(name)
        try:
            logger = touch_logger(name)
            handlers = logger.handlers[:]
            for handler in handlers:
                logger.removeHandler(handler)
                handler.close()
            if logger.name in logging.Logger.manager.loggerDict:
                logging.Logger.manager.loggerDict.pop(logger.name)
        except Exception:
            pass
    
    @property
    def current_logger(self) -> logging.Logger:
        try:
            current_task = asyncio.current_task()
            current_name = current_task.get_name() if current_task else "GLOBAL"
            if(current_name not in self.record):
                logger = self.register(current_name)
                return logger
            self.record[current_name] = time.time()
            return touch_logger(name=current_name)
        except RuntimeError:
            return self.logger
        except Exception:
            return self.secondary_logger
    
    def debug(self, msg:object) -> None:
        msg_s = self._obj2str(msg)
        self.current_logger.debug(msg_s, stacklevel=2)
    
    def info(self, msg:object) -> None:
        msg_s = self._obj2str(msg)
        self.current_logger.info(msg_s, stacklevel=2)
    
    def warning(self, msg:object) -> None:
        msg_s = self._obj2str(msg)
        self.current_logger.warning(msg_s, stacklevel=2)
    
    def error(self, msg:object) -> None:
        msg_s = self._obj2str(msg)
        self.current_logger.error(msg_s, stacklevel=2)
    
    def critical(self, msg:object) -> None:
        msg_s = self._obj2str(msg)
        self.current_logger.critical(msg_s, stacklevel=2)
    
    def _obj2str(self, obj:object) -> str:
        match obj:
            case str():
                return obj
            case int() | float() | bool():
                return str(obj)
            case _:
                return str(obj)
            
logger = LoggerManager()