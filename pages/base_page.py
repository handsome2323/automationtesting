# pages/base_page.py - 页面对象模型基础类
# Page Object Model (POM) 是UI自动化测试的最佳实践
# 将页面元素和操作分离，便于维护和复用

from playwright.async_api import Page
from utils.logger import setup_logger
from utils.config import Config

logger = setup_logger(__name__)


class BasePage:
    """
    所有页面的基础类
    包含通用的页面操作和元素交互方法
    
    使用方法:
        class LoginPage(BasePage):
            LOGIN_BUTTON = "#login-btn"
            
            async def click_login(self):
                await self.click(self.LOGIN_BUTTON)
    """
    
    def __init__(self, page: Page):
        """
        初始化基础页面
        
        Args:
            page: Playwright Page 对象
        """
        self.page = page
        self.logger = logger
    
    # ====== 基础导航操作 ======
    
    async def goto(self, url: str):
        """
        导航到指定URL
        
        Args:
            url: 完整URL或路径
        
        使用示例:
            await page.goto("https://example.com/login")
            await page.goto("/login")  # 相对路径
        """
        full_url = url if url.startswith("http") else f"{Config.BASE_URL}{url}"
        self.logger.info(f"📍 导航到: {full_url}")
        await self.page.goto(full_url, wait_until="networkidle")
    
    async def get_current_url(self) -> str:
        """
        获取当前页面URL
        
        Returns:
            当前页面的完整URL
        """
        url = self.page.url
        self.logger.debug(f"当前URL: {url}")
        return url
    
    async def get_page_title(self) -> str:
        """
        获取页面标题
        
        Returns:
            页面的<title>标签内容
        """
        title = await self.page.title()
        self.logger.debug(f"页面标题: {title}")
        return title
    
    # ====== 元素交互操作 ======
    
    async def click(self, selector: str):
        """
        点击元���
        
        Args:
            selector: CSS选择器
        
        使用示例:
            await page.click("#submit-btn")
            await page.click("button:has-text('登录')")
        """
        self.logger.debug(f"🖱️ 点击: {selector}")
        await self.page.click(selector)
    
    async def fill(self, selector: str, text: str):
        """
        填充输入框
        
        Args:
            selector: CSS选择器
            text: 要输入的文本
        
        使用示例:
            await page.fill("#username", "testuser")
            await page.fill("input[name='email']", "test@example.com")
        """
        self.logger.debug(f"⌨️ 输入到 {selector}: {text}")
        await self.page.fill(selector, text)
    
    async def clear(self, selector: str):
        """
        清空输入框
        
        Args:
            selector: CSS选择器
        """
        self.logger.debug(f"🧹 清空: {selector}")
        await self.page.fill(selector, "")
    
    async def type_text(self, selector: str, text: str, delay: int = 0):
        """
        逐个输入字符（模拟真实用户输入）
        
        Args:
            selector: CSS选择器
            text: 要输入的文本
            delay: 每个字符的延迟（毫秒）
        
        使用示例:
            # 模拟真实用户缓慢输入
            await page.type_text("#password", "SecurePass123", delay=50)
        """
        self.logger.debug(f"✍️ 慢速输入到 {selector}: {text}")
        await self.page.locator(selector).type(text, delay=delay)
    
    async def select_option(self, selector: str, option: str):
        """
        在下拉框中选择选项
        
        Args:
            selector: CSS选择器
            option: 选项值或文本
        
        使用示例:
            await page.select_option("select#country", "US")
            await page.select_option("select#country", "United States")
        """
        self.logger.debug(f"🔽 选择: {selector} = {option}")
        await self.page.select_option(selector, option)
    
    async def check(self, selector: str):
        """
        勾选复选框
        
        Args:
            selector: CSS选择器
        
        使用示例:
            await page.check("#agree-terms")
        """
        self.logger.debug(f"☑️ 勾选: {selector}")
        await self.page.check(selector)
    
    async def uncheck(self, selector: str):
        """
        取消勾选复选框
        
        Args:
            selector: CSS选择器
        """
        self.logger.debug(f"☐ 取消勾选: {selector}")
        await self.page.uncheck(selector)
    
    # ====== 元素查询操作 ======
    
    async def get_text(self, selector: str) -> str:
        """
        获取元素文本内容
        
        Args:
            selector: CSS选择器
        
        Returns:
            元素的文本内容
        
        使用示例:
            title = await page.get_text("h1")
            print(title)  # 输出: \"欢迎来到我的网站\"
        """
        text = await self.page.text_content(selector)
        self.logger.debug(f"📖 获取文本 {selector}: {text}")
        return text.strip() if text else ""
    
    async def get_attribute(self, selector: str, attr: str) -> str:
        """
        获取元素的属性值
        
        Args:
            selector: CSS选择器
            attr: 属性名
        
        Returns:
            属性值
        
        使用示例:
            href = await page.get_attribute("a.link", "href")
            print(href)  # 输出: \"https://example.com\"
            
            placeholder = await page.get_attribute("#username", "placeholder")
            print(placeholder)  # 输出: \"请输入用户名\"
        """
        value = await self.page.get_attribute(selector, attr)
        self.logger.debug(f"🏷️ 获取属性 {selector}[{attr}]: {value}")
        return value if value else ""
    
    async def get_input_value(self, selector: str) -> str:
        """
        获取输入框的值
        
        Args:
            selector: CSS选择器
        
        Returns:
            输入框的值
        
        使用示例:
            value = await page.get_input_value("#email")
            print(value)
        """
        value = await self.get_attribute(selector, "value")
        self.logger.debug(f"📝 获取输入值 {selector}: {value}")
        return value
    
    # ====== 元素状态检查 ======
    
    async def is_visible(self, selector: str) -> bool:
        """
        检查元素是否可见
        
        Args:
            selector: CSS选择器
        
        Returns:
            True 如果元素可见
        
        使用示例:
            if await page.is_visible(".success-message"):
                print("成功消息可见")
        """
        is_visible = await self.page.is_visible(selector)
        self.logger.debug(f"👁️ 元素可见性 {selector}: {is_visible}")
        return is_visible
    
    async def is_enabled(self, selector: str) -> bool:
        """
        检查元素是否启用
        
        Args:
            selector: CSS选择器
        
        Returns:
            True 如果元素启用
        """
        is_enabled = await self.page.is_enabled(selector)
        self.logger.debug(f"⚙️ 元素启用状态 {selector}: {is_enabled}")
        return is_enabled
    
    async def is_checked(self, selector: str) -> bool:
        """
        检查复选框是否被勾选
        
        Args:
            selector: CSS选择器
        
        Returns:
            True 如果被勾选
        """
        is_checked = await self.page.is_checked(selector)
        self.logger.debug(f"✔️ 复选框状态 {selector}: {is_checked}")
        return is_checked
    
    # ====== 等待操作 ======
    
    async def wait_for_selector(self, selector: str, timeout: int = None):
        """
        等待元素出现
        
        Args:
            selector: CSS选择器
            timeout: 超时时间（秒）
        
        使用示例:
            await page.wait_for_selector(".loading-complete", timeout=10)
        """
        timeout_ms = (timeout or Config.WAIT_TIME) * 1000
        self.logger.debug(f"⏳ 等待元素: {selector}")
        await self.page.wait_for_selector(selector, timeout=timeout_ms)
    
    async def wait_for_url_change(self, timeout: int = None):
        """
        等待URL变化
        
        Args:
            timeout: 超时时间（秒）
        
        使用示例:
            await page.click("#logout-btn")
            await page.wait_for_url_change()
        """
        timeout_ms = (timeout or Config.WAIT_TIME) * 1000
        old_url = self.page.url
        self.logger.debug(f"⏳ 等待URL变化...")
        await self.page.wait_for_function(
            f"window.location.href !== '{old_url}'",
            timeout=timeout_ms
        )
    
    # ====== 页面交互 ======
    
    async def reload(self):
        """
        刷新页面
        
        使用示例:
            await page.reload()
        """
        self.logger.info("🔄 刷新页面")
        await self.page.reload()
    
    async def go_back(self):
        """
        返回上一页
        
        使用示例:
            await page.go_back()
        """
        self.logger.info("⬅️ 返回上一页")
        await self.page.go_back()
    
    async def go_forward(self):
        """
        前进到下一页
        
        使用示例:
            await page.go_forward()
        """
        self.logger.info("➡️ 前进到下一页")
        await self.page.go_forward()
    
    # ====== 截图 ======
    
    async def take_screenshot(self, filename: str):
        """
        保存页面截图
        
        Args:
            filename: 文件名
        
        使用示例:
            await page.take_screenshot("login_page.png")
        """
        from pathlib import Path
        filepath = Config.SCREENSHOTS_DIR / filename
        self.logger.info(f"📸 保存截图: {filename}")
        await self.page.screenshot(path=filepath, full_page=True)
    
    async def scroll_to_bottom(self):
        """
        滚动到页面底部
        
        使用示例:
            await page.scroll_to_bottom()
        """
        self.logger.debug("⬇️ 滚动到页面底部")
        await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
