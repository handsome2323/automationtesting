# utils/logger.py - 日志记录模块
# 提供统一的日志配置和记录功能

import logging
import logging.handlers
from pathlib import Path
from datetime import datetime
from utils.config import Config

# 创建logs目录
Config.LOGS_DIR.mkdir(exist_ok=True)


def setup_logger(name: str) -> logging.Logger:
    """
    配置并返回日志记录器
    
    Args:
        name: 日志记录器名称（通常使用 __name__）
    
    Returns:
        配置好的Logger对象
    
    使用方法:
        from utils.logger import setup_logger
        logger = setup_logger(__name__)
        logger.info("这是一条信息日志")
        logger.error("这是一条错误日志")
    """
    
    logger = logging.getLogger(name)
    
    # 如果已经配置过，直接返回
    if logger.handlers:
        return logger
    
    # 设置日志级别
    log_level = getattr(logging, Config.LOG_LEVEL.upper())
    logger.setLevel(log_level)
    
    # 日志格式
    log_format = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # ====== 控制台处理器 (Console Handler) ======
    # 将日志输出到控制台（终端）
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)
    
    # ====== 文件处理器 (File Handler) ======
    # 将日志输出到文件，支持滚动（文件大小超过限制时自动创建新文件）
    file_handler = logging.handlers.RotatingFileHandler(
        filename=Config.LOG_FILE,
        maxBytes=10 * 1024 * 1024,  # 最大10MB
        backupCount=5,               # 保留5个备份文件
        encoding='utf-8'
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)
    
    return logger


# 创建全局日志记录器
logger = setup_logger(__name__)


class TestLogger:
    """
    测试相关的日志记录器
    提供测试特定的日志方法
    """
    
    def __init__(self):
        self.logger = setup_logger("TestLogger")
    
    def step(self, step_num: int, description: str):
        """
        记录测试步骤
        
        Args:
            step_num: 步骤序号
            description: 步骤描述
        """
        self.logger.info(f"\n【步骤 {step_num}】{description}")
    
    def assert_result(self, condition: bool, message: str):
        """
        记录断言结果
        
        Args:
            condition: 断言条件
            message: 提示信息
        """
        if condition:
            self.logger.info(f"✅ 断言成功: {message}")
        else:
            self.logger.error(f"❌ 断言失败: {message}")
    
    def info(self, message: str):
        """记录信息日志"""
        self.logger.info(f"ℹ️  {message}")
    
    def success(self, message: str):
        """记录成功日志"""
        self.logger.info(f"✅ {message}")
    
    def error(self, message: str):
        """记录错误日志"""
        self.logger.error(f"❌ {message}")
    
    def warning(self, message: str):
        """记录警告日志"""
        self.logger.warning(f"⚠️  {message}")
    
    def debug(self, message: str):
        """记录调试日志"""
        self.logger.debug(f"🔍 {message}")


# ============================================================================
# 使用示例
# ============================================================================

if __name__ == "__main__":
    # 使用方式1: 直接使用全局logger
    logger.info("这是一条信息")
    logger.error("这是一条错误")
    
    # 使用方式2: 创建特定的logger
    test_logger = TestLogger()
    test_logger.step(1, "打开网站")
    test_logger.step(2, "输入用户名")
    test_logger.success("登录成功")
    test_logger.assert_result(True, "验证页面标题")
