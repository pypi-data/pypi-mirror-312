import os
import logging
from logging.handlers import RotatingFileHandler
from threading import Lock
from datetime import datetime

class Logger:
    _instance = None  # 单例实例
    _lock = Lock()    # 用于线程安全

    def __new__(cls, *args, **kwargs):
        """
        创建单例实例
        """
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, log_name: str = "application", log_level=logging.INFO):
        """
        初始化 Logger
        :param log_name: 日志名称（默认 "application"）
        :param log_level: 日志级别（默认 INFO）
        """
        if not hasattr(self, "_initialized"):  # 确保只初始化一次
            self._initialized = True
            self.log_name = log_name
            self.log_level = log_level

            # 创建基于日期时间的日志文件夹
            self.log_dir = self._create_log_folder()
            self.logger = self._setup_logger()

    def _create_log_folder(self):
        """
        创建基于日期和时间命名的日志文件夹
        :return: 日志文件夹路径
        """
        current_time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        log_folder = os.path.join(os.getcwd(), f'log-{current_time}')
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)
        return log_folder

    def _setup_logger(self):
        """
        配置 Logger
        :return: 配置好的 Logger 对象
        """
        logger = logging.getLogger(self.log_name)
        logger.setLevel(self.log_level)

        # 防止重复添加 Handlers
        if not logger.handlers:
            # 日志格式
            formatter = logging.Formatter(
                "[%(asctime)s] %(levelname)s - %(message)s"
            )

            # 创建不同级别的日志处理器
            self._create_log_handler(logger, logging.INFO, "INFO.log", formatter)
            self._create_log_handler(logger, logging.WARNING, "WARNING.log", formatter)
            self._create_log_handler(logger, logging.ERROR, "ERROR.log", formatter)

        return logger

    def _create_log_handler(self, logger, level, filename, formatter):
        """
        为不同级别的日志创建处理器
        :param logger: logger对象
        :param level: 日志级别
        :param filename: 日志文件名
        :param formatter: 日志格式
        """
        log_file_path = os.path.join(self.log_dir, filename)
        file_handler = RotatingFileHandler(
            log_file_path, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    def get_logger(self):
        """
        返回 Logger 对象
        :return: Logger
        """
        return self.logger

    def log_info(self, message: str):
        """记录 INFO 级别日志"""
        self.logger.info(message)

    def log_warning(self, message: str):
        """记录 WARNING 级别日志"""
        self.logger.warning(message)

    def log_error(self, message: str):
        """记录 ERROR 级别日志"""
        self.logger.error(message)

    def log_exception(self, exception: Exception):
        """记录异常错误日志"""
        self.logger.error("Exception occurred", exc_info=exception)
