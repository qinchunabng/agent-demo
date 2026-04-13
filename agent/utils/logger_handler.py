try:
    from utils.path_tool import get_abs_path
except ImportError:
    try:
        from agent.utils.path_tool import get_abs_path
    except ImportError:
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from utils.path_tool import get_abs_path

import os
import logging
from datetime import datetime


# 日志保存的根目录
LOG_ROOT = get_abs_path("logs")

# 确保日志目录存在
os.makedirs(LOG_ROOT, exist_ok=True)

# 日志的格式配置
DEFAULT_LOG_FORMAT = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s")

def get_logger(
    name: str = "agent",
    console_level: str = "INFO",
    file_level: str = "INFO",
    log_file: str = None,
) -> logging.Logger:
    """
    获取日志记录器
    """
    logger = logging.getLogger(name)
    logger.setLevel(file_level)
    
    # 避免重复添加处理器
    if logger.handlers:
        return logger
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(DEFAULT_LOG_FORMAT)
    logger.addHandler(console_handler)
    
    # 文件handler
    if not log_file:
        log_file = os.path.join(LOG_ROOT, f"{name}-{datetime.now().strftime('%Y%m%d')}.log")

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(file_level)
    file_handler.setFormatter(DEFAULT_LOG_FORMAT)
    logger.addHandler(file_handler)
    
    return logger

logger = get_logger()

if __name__ == "__main__":
    logger.info("这是一条info日志")
    logger.error("这是一条error日志")
