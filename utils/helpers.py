# utils/helpers.py - 辅助函数工具模块
# 提供通用的帮助函数，供测试代码使用

import asyncio
import time
from typing import Any, Callable, Optional
from datetime import datetime
from playwright.async_api import Page, Locator
from utils.logger import setup_logger

logger = setup_logger(__name__)


# ============================================================================
# 等待相关函数
# ============================================================================

async def wait_for_element(
    page: Page,
    selector: str,
    timeout: int = 10,
    state: str = "visible"
) -> Locator:
    """
    等待元素出现（显式等待）
    
    Args:
        page: Playwright页面对象
        selector: CSS选择器
        timeout: 等待超时时间（秒）
        state: 元素状态 - "visible" (可见), "attached" (存在), "hidden" (隐藏)
    
    Returns:
        元素的Locator对象
    
    使用示例:
        button = await wait_for_element(page, "#submit-btn", timeout=5)
        await button.click()
    """
    try:
        logger.debug(f"等待元素: {selector}, 状态: {state}")
        locator = page.locator(selector)
        await locator.wait_for(state=state, timeout=timeout * 1000)
        logger.debug(f"✅ 元素已找到: {selector}")
        return locator
    except Exception as e:
        logger.error(f"❌ 等待元素失败: {selector} - {str(e)}")
        raise


async def wait_for_url(
    page: Page,
    url_pattern: str,
    timeout: int = 10
):
    """
    等待页面URL符合特定模式
    
    Args:
        page: Playwright页面对象
        url_pattern: URL正则表达式或字符串
        timeout: 等待超时时间（秒）
    
    使用示例:
        await wait_for_url(page, ".*example.com.*login.*")
    """
    try:
        logger.debug(f"等待页面URL: {url_pattern}")
        await page.wait_for_url(url_pattern, timeout=timeout * 1000)
        logger.debug(f"✅ URL已加载: {page.url}")
    except Exception as e:
        logger.error(f"❌ URL等待失败 - {str(e)}")
        raise


async def wait_for_navigation(
    page: Page,
    action: Callable,
    timeout: int = 10
):
    """
    在执行某个操作时等待页面导航完成
    
    Args:
        page: Playwright页面对象
        action: 触发导航的异步函数
        timeout: 等待超时时间（秒）
    
    使用示例:
        async def click_login():
            await page.click("#login-btn")
        
        await wait_for_navigation(page, click_login)
    """
    try:
        logger.debug("等待页面导航...")
        async with page.expect_navigation(timeout=timeout * 1000):
            await action()
        logger.debug(f"✅ 页面导航完成，新URL: {page.url}")
    except Exception as e:
        logger.error(f"❌ 页面导航超时 - {str(e)}")
        raise


# ============================================================================
# 输入相关函数
# ============================================================================

async def fill_input(
    page: Page,
    selector: str,
    text: str,
    clear: bool = True,
    delay: int = 0
):
    """
    填充输入框
    
    Args:
        page: Playwright页面对象
        selector: CSS选择器
        text: 要填充的文本
        clear: 是否先清空输入框
        delay: 输入延迟（毫秒），用于模拟真实用户输入
    
    使用示例:
        await fill_input(page, "#username", "testuser", delay=50)
    """
    try:
        logger.debug(f"填充输入框: {selector} = {text}")
        locator = page.locator(selector)
        
        if clear:
            await locator.clear()
        
        if delay > 0:
            # 逐个字符输入，模拟真实用户
            for char in text:
                await locator.type(char, delay=delay)
        else:
            await locator.fill(text)
        
        logger.debug(f"✅ 输入完成: {selector}")
    except Exception as e:
        logger.error(f"❌ 输入失败: {selector} - {str(e)}")
        raise


async def click_element(
    page: Page,
    selector: str,
    delay: int = 0
):
    """
    点击元素
    
    Args:
        page: Playwright页面对象
        selector: CSS选择器
        delay: 点击前延迟（毫秒）
    
    使用示例:
        await click_element(page, "#submit-btn")
    """
    try:
        logger.debug(f"点击元素: {selector}")
        locator = page.locator(selector)
        
        if delay > 0:
            await asyncio.sleep(delay / 1000)
        
        await locator.click()
        logger.debug(f"✅ 点击成功: {selector}")
    except Exception as e:
        logger.error(f"❌ 点击失败: {selector} - {str(e)}")
        raise


# ============================================================================
# 获取数据函数
# ============================================================================

async def get_text(
    page: Page,
    selector: str
) -> str:
    """
    获取元素的文本内容
    
    Args:
        page: Playwright页面对象
        selector: CSS选择器
    
    Returns:
        元素的文本内容
    
    使用示例:
        title = await get_text(page, "h1")
        print(title)
    """
    try:
        text = await page.locator(selector).text_content()
        logger.debug(f"获取文本: {selector} = {text}")
        return text.strip() if text else ""
    except Exception as e:
        logger.error(f"❌ 获取文本失败: {selector} - {str(e)}")
        raise


async def get_attribute(
    page: Page,
    selector: str,
    attribute: str
) -> str:
    """
    获取元素的属性值
    
    Args:
        page: Playwright页面对象
        selector: CSS选择器
        attribute: 属性名（如 href, value, placeholder等）
    
    Returns:
        属性值
    
    使用示例:
        href = await get_attribute(page, "a.link", "href")
        print(href)  # 输出: https://example.com
    """
    try:
        value = await page.locator(selector).get_attribute(attribute)
        logger.debug(f"获取属性: {selector}[{attribute}] = {value}")
        return value if value else ""
    except Exception as e:
        logger.error(f"❌ 获取属性失败: {selector}[{attribute}] - {str(e)}")
        raise


async def is_element_visible(
    page: Page,
    selector: str
) -> bool:
    """
    检查元素是否可见
    
    Args:
        page: Playwright页面对象
        selector: CSS选择器
    
    Returns:
        True if 元素可见，False if 不可见
    
    使用示例:
        if await is_element_visible(page, ".success-message"):
            print("成功信息可见")
    """
    try:
        is_visible = await page.locator(selector).is_visible()
        logger.debug(f"检查元素可见性: {selector} = {is_visible}")
        return is_visible
    except Exception as e:
        logger.debug(f"元素不可见: {selector}")
        return False


# ============================================================================
# 截图函数
# ============================================================================

async def take_screenshot(
    page: Page,
    filename: str
):
    """
    保存页面截图
    
    Args:
        page: Playwright页面对象
        filename: 保存文件名
    
    使用示例:
        await take_screenshot(page, "login_page.png")
    """
    try:
        from pathlib import Path
        from utils.config import Config
        
        filepath = Config.SCREENSHOTS_DIR / filename
        await page.screenshot(path=filepath, full_page=True)
        logger.info(f"✅ 截图已保存: {filepath}")
    except Exception as e:
        logger.error(f"❌ 截图失败 - {str(e)}")
        raise


# ============================================================================
# 页面操作函数
# ============================================================================

async def scroll_to_bottom(page: Page):
    """
    滚动到页面底部
    
    使用示例:
        await scroll_to_bottom(page)
    """
    try:
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        logger.debug("✅ 已滚动到页面底部")
        await asyncio.sleep(0.5)  # 等待延迟加载
    except Exception as e:
        logger.error(f"❌ 滚动失败 - {str(e)}")
        raise


async def scroll_to_element(
    page: Page,
    selector: str
):
    """
    滚动到指定元素
    
    使用示例:
        await scroll_to_element(page, "#footer")
    """
    try:
        await page.locator(selector).scroll_into_view_if_needed()
        logger.debug(f"✅ 已滚动到元素: {selector}")
    except Exception as e:
        logger.error(f"❌ 滚动失败 - {str(e)}")
        raise


async def select_option(
    page: Page,
    selector: str,
    label_or_value: str
):
    """
    在下拉选择框中选择选项
    
    Args:
        page: Playwright页面对象
        selector: CSS选择器
        label_or_value: 选项标签或值
    
    使用示例:
        await select_option(page, "select#country", "United States")
    """
    try:
        await page.locator(selector).select_option(label_or_value)
        logger.debug(f"✅ 已选择: {selector} = {label_or_value}")
    except Exception as e:
        logger.error(f"❌ 选择失败: {selector} - {str(e)}")
        raise


# ============================================================================
# 使用示例
# ============================================================================

if __name__ == "__main__":
    print("这是辅助函数模块，用于测试中导入")
    print("\n可用函数列表:")
    print("  等待: wait_for_element, wait_for_url, wait_for_navigation")
    print("  输入: fill_input, click_element")
    print("  获取: get_text, get_attribute, is_element_visible")
    print("  其他: take_screenshot, scroll_to_bottom, select_option")
