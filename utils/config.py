# utils/config.py - 项目配置管理
# 集中管理所有配置，便于修改和管理

import os
from pathlib import Path
from dotenv import load_dotenv

# 加载 .env 环境变量文件
load_dotenv()


class Config:
    """
    项目全局配置类
    
    使用方法:
        from utils.config import Config
        url = Config.BASE_URL
        headless = Config.HEADLESS
    """
    
    # ====== 项目路径配置 ======
    PROJECT_ROOT = Path(__file__).parent.parent
    SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots"
    REPORTS_DIR = PROJECT_ROOT / "reports"
    LOGS_DIR = PROJECT_ROOT / "logs"
    
    # ====== 浏览器配置 ======
    # 无头模式（不显示浏览器窗口），可在命令行用 --headless 覆盖
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    
    # 执行速度减速（毫秒），用于调试时观察操作过程
    SLOW_MO = int(os.getenv("SLOW_MO", "0"))
    
    # 浏览器类型: chromium, firefox, webkit
    BROWSER_TYPE = os.getenv("BROWSER_TYPE", "chromium")
    
    # 浏览器视口大小
    VIEWPORT_WIDTH = int(os.getenv("VIEWPORT_WIDTH", "1920"))
    VIEWPORT_HEIGHT = int(os.getenv("VIEWPORT_HEIGHT", "1080"))
    
    # ====== 网站URL配置 ======
    # 测试网站的基础URL
    BASE_URL = os.getenv("BASE_URL", "https://example.com")
    
    # 各页面URL
    LOGIN_URL = os.getenv("LOGIN_URL", f"{BASE_URL}/login")
    HOME_URL = os.getenv("HOME_URL", f"{BASE_URL}/home")
    PRODUCT_URL = os.getenv("PRODUCT_URL", f"{BASE_URL}/products")
    
    # ====== API配置 ======
    # API服务的基础URL
    API_BASE_URL = os.getenv("API_BASE_URL", "https://api.example.com")
    
    # API版本
    API_VERSION = os.getenv("API_VERSION", "v1")
    
    # API超时时间（秒）
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", "10"))
    
    # ====== 认证配置 ======
    # 测试账号
    TEST_USERNAME = os.getenv("TEST_USERNAME", "testuser@example.com")
    TEST_PASSWORD = os.getenv("TEST_PASSWORD", "TestPassword123!")
    
    # API Token（如果需要）
    API_TOKEN = os.getenv("API_TOKEN", "")
    
    # ====== 等待配置 ======
    # 显式等待的最大时间（秒）
    WAIT_TIME = int(os.getenv("WAIT_TIME", "10"))
    
    # 隐式等待时间（秒）
    IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "5"))
    
    # ====== 日志配置 ======
    # 日志级别: DEBUG, INFO, WARNING, ERROR, CRITICAL
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # 日志文件路径
    LOG_FILE = LOGS_DIR / "test.log"
    
    # ====== 测试配置 ======
    # 失败时是否保存截图
    SAVE_SCREENSHOT_ON_FAILURE = os.getenv("SAVE_SCREENSHOT_ON_FAILURE", "true").lower() == "true"
    
    # 失败重试次数
    RETRY_COUNT = int(os.getenv("RETRY_COUNT", "1"))
    
    # 是否在CI环境中运行
    IS_CI = os.getenv("CI", "false").lower() == "true"
    
    # ====== 环境 ======
    ENV = os.getenv("ENV", "dev")  # dev, staging, prod
    
    @classmethod
    def print_config(cls):
        """
        打印当前配置信息（用于调试）
        """
        print("\n" + "="*60)
        print("当前测试配置")
        print("="*60)
        print(f"环境: {cls.ENV}")
        print(f"基础URL: {cls.BASE_URL}")
        print(f"API URL: {cls.API_BASE_URL}")
        print(f"无头模式: {cls.HEADLESS}")
        print(f"浏览器: {cls.BROWSER_TYPE}")
        print(f"视口大小: {cls.VIEWPORT_WIDTH}x{cls.VIEWPORT_HEIGHT}")
        print(f"等待超时: {cls.WAIT_TIME}秒")
        print(f"日志级别: {cls.LOG_LEVEL}")
        print("="*60 + "\n")


# ============================================================================
# 使用示例
# ============================================================================

if __name__ == "__main__":
    # 打印配置
    Config.print_config()
    
    # 访问配置
    print(f"登录URL: {Config.LOGIN_URL}")
    print(f"等待时间: {Config.WAIT_TIME}秒")
