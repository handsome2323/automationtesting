# conftest.py - pytest的全局配置文件
# 这个文件会在运行pytest时自动加载
# 用于定义共享的fixtures（测试装置）和配置

import pytest
import os
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright, Browser, BrowserContext, Page

# 导入自定义配置和日志
from utils.config import Config
from utils.logger import setup_logger

# 创建日志记录器
logger = setup_logger(__name__)

# ============================================================================
# 项目根目录定义
# ============================================================================
PROJECT_ROOT = Path(__file__).parent
SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots"
REPORTS_DIR = PROJECT_ROOT / "reports"


def pytest_configure(config):
    """
    pytest启动钩子 - 在pytest开始执行前运行
    用于创建必要的目录、初始化配置等
    """
    # 创建截图和报告目录
    SCREENSHOTS_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)
    
    logger.info(f"测试开始执行 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"项目根目录: {PROJECT_ROOT}")


def pytest_collection_modifyitems(config, items):
    """
    pytest收集测试用例后的钩子
    用于修改测试用例的执行顺序、标记等
    """
    # 为所有测试添加timeout标记（防止无限等待）
    for item in items:
        item.add_marker(pytest.mark.timeout(30))  # 30秒超时


# ============================================================================
# UI测试 Fixtures (Playwright)
# ============================================================================

@pytest.fixture(scope="function")
async def browser():
    """
    Fixture: 浏览器实例
    scope="function" 表示每个测试函数都会创建新的浏览器实例
    
    使用方法:
        async def test_something(browser):
            page = await browser.new_page()
    """
    playwright = await async_playwright().start()
    # 启动浏览器 (chromium/firefox/webkit)
    browser_instance = await playwright.chromium.launch(
        headless=Config.HEADLESS,  # 无头模式（不显示浏览器窗口）
        slow_mo=Config.SLOW_MO,     # 减速执行（毫秒）
    )
    yield browser_instance
    
    # 清理资源
    await browser_instance.close()
    await playwright.stop()


@pytest.fixture(scope="function")
async def context(browser: Browser):
    """
    Fixture: 浏览器上下文
    一个context可以包含多个page，共享cookies和storage
    
    使用方法:
        async def test_something(context):
            page = await context.new_page()
    """
    ctx = await browser.new_context(
        viewport={"width": 1920, "height": 1080},  # 设置视口大小
        ignore_https_errors=True,                   # 忽略HTTPS错误
    )
    yield ctx
    await ctx.close()


@pytest.fixture(scope="function")
async def page(context: BrowserContext):
    """
    Fixture: 页面实例
    这是最常用的fixture，代表一个浏览器标签页
    
    使用方法:
        async def test_login(page):
            await page.goto("https://example.com")
    """
    page_instance = await context.new_page()
    
    # 添加日志监听器
    page_instance.on("console", lambda msg: logger.debug(f"浏览器控制台: {msg.text}"))
    page_instance.on("crash", lambda: logger.error("页面崩溃!"))
    
    yield page_instance
    
    # 测试失败时保存截图
    # （这部分在request fixture中实现）
    await page_instance.close()


# ============================================================================
# 测试结果钩子
# ============================================================================

@pytest.fixture(scope="function")
def request_fixture(request):
    """
    获取当前测试的request对象，用于处理测试失败
    """
    yield request
    
    # 如果测试失败
    if request.node.rep_call.failed:
        logger.error(f"❌ 测试失败: {request.node.name}")


def pytest_runtest_makereport(item, call):
    """
    pytest钩子 - 在测试执行后调用
    用于收集测试结果信息
    """
    if call.excinfo is not None:
        logger.error(f"异常信息: {call.excinfo.typename} - {call.excinfo.value}")


# ============================================================================
# 命令行选项
# ============================================================================

def pytest_addoption(parser):
    """
    为pytest添加自定义命令行选项
    
    使用方法:
        pytest --headless  # 无头模式运行
        pytest --slow-mo 100  # 减速100ms
    """
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="以无头模式运行浏览器"
    )
    parser.addoption(
        "--slow-mo",
        action="store",
        default=0,
        type=int,
        help="减速执行（毫秒）"
    )
    parser.addoption(
        "--base-url",
        action="store",
        default=Config.BASE_URL,
        help="测试网站的基础URL"
    )


def pytest_configure_after_cmdline(config):
    """
    在命令行解析后更新配置
    """
    if config.getoption("--headless"):
        Config.HEADLESS = True
    if config.getoption("--slow-mo"):
        Config.SLOW_MO = config.getoption("--slow-mo")


# ============================================================================
# 标记定义 (Markers)
# ============================================================================

def pytest_configure(config):
    """
    定义自定义markers，用于标记和选择测试
    """
    config.addinivalue_line(
        "markers", "smoke: 冒烟测试（快速基础功能测试）"
    )
    config.addinivalue_line(
        "markers", "regression: 回归测试（完整功能测试）"
    )
    config.addinivalue_line(
        "markers", "slow: 慢速测试"
    )
    config.addinivalue_line(
        "markers", "skip_ci: 在CI环境中跳过"
    )


# ============================================================================
# 测试会话钩子
# ============================================================================

def pytest_sessionfinish(session, exitstatus):
    """
    pytest会话结束时调用
    用于生成汇总信息、清理资源等
    """
    logger.info(f"测试执行完毕 - 状态码: {exitstatus}")
    logger.info("═" * 60)
