import logging
import os
from lljz_tools.log_manager import LogManager, Formatter, BaseFormatter, ColoredFormatter, default_fmt 
from pathlib import Path
import sys
from typing import Optional

logger = LogManager(
    'EASY_API_TEST',
    console_level='INFO',
    file_path=str(Path.home() / 'pythonlogs'),  # 默认使用家目录下的pythonlogs目录
    file_level='INFO',
    error_level='ERROR',
).get_logger()


def init_logger(
    console_level: str = 'DEBUG', 
    file_level: str = 'DEBUG', 
    file_path: str = str(Path.home() / 'pythonlogs'),
    colorize: bool = True,
    fmt: Optional[str] = None
):
    file = os.path.join(file_path, 'out.log')
    error_file = os.path.join(file_path, 'error.log')
    fmt = fmt or default_fmt
    logger.remove()
    if not logger.handlers:
        style = LogManager._guess_fmt_style(fmt)
        file_format = Formatter(fmt, style=style)  # 文件中的日志格式
        
        # 控制台中的日志格式
        if not colorize:
            console_format = BaseFormatter(fmt=fmt, style=style)
        else:
            console_format = ColoredFormatter(fmt=fmt, style=style)
        
        # 添加日志处理器--控制台
        logger.add(sys.stdout, level=console_level, formatter=console_format)

        # 添加日志处理器--文件
        logger.add(file, level=file_level, formatter=file_format, filters=lambda record: record.levelno < logging.ERROR)
        
        # 添加日志处理器--错误文件
        logger.add(error_file, level='ERROR', formatter=file_format)
    return logger

if __name__ == '__main__':
    pass
