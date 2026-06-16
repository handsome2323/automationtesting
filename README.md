# 自动化测试学习项目

这是一个完整的 **UI自动化测试** 和 **API测试** 学习项目，使用 Python + Playwright + Requests。

## 📁 项目结构

```
automationtesting/
├── tests/                          # 测试用例目录
│   ├── ui_tests/                   # UI自动化测试
│   │   ├── test_login.py          # 登录功能测试
│   │   ├── test_product.py        # 产品页面测试
│   │   └── test_checkout.py       # 购物流程测试
│   └── api_tests/                  # API接口测试
│       ├── test_user_api.py       # 用户API测试
│       ├── test_product_api.py    # 产品API测试
│       └── test_order_api.py      # 订单API测试
├── pages/                          # 页面对象模型 (POM)
│   ├── base_page.py               # 基础页面类
│   ├── login_page.py              # 登录页面
│   ├── product_page.py            # 产品页面
│   └── checkout_page.py           # 购物结算页面
├── api/                            # API请求相关
│   ├── base_api.py                # 基础API类
│   ├── user_api.py                # 用户API
│   ├── product_api.py             # 产品API
│   └── order_api.py               # 订单API
├── utils/                          # 工具类
│   ├── logger.py                  # 日志配置
│   ├── config.py                  # 配置管理
│   └── helpers.py                 # 辅助函数
├── reports/                        # 测试报告目录（自动生成）
├── screenshots/                    # 失败截图目录（自动生成）
├── conftest.py                     # pytest配置文件
├── requirements.txt                # 项目依赖
└── pytest.ini                      # pytest配置
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行所有测试

```bash
pytest
```

### 3. 运行特定测试

```bash
# 运行UI测试
pytest tests/ui_tests/

# 运行API测试
pytest tests/api_tests/

# 运行特定文件
pytest tests/ui_tests/test_login.py

# 运行特定测试类
pytest tests/ui_tests/test_login.py::TestLogin

# 运行特定测试方法
pytest tests/ui_tests/test_login.py::TestLogin::test_valid_login
```

### 4. 生成HTML测试报告

```bash
pytest --html=reports/report.html --self-contained-html
```

## 📚 学习重点

### UI自动化测试
- ✅ Playwright基础使用
- ✅ 页面对象模型(POM)设计模式
- ✅ 元素定位策略
- ✅ 等待机制(显式等待、隐式等待)
- ✅ 截图和日志记录
- ✅ 失败重试机制

### API测试
- ✅ HTTP请求方法 (GET, POST, PUT, DELETE)
- ✅ 请求头和请求体处理
- ✅ 响应验证
- ✅ 状态码检查
- ✅ JSON格式数据验证
- ✅ API链式调用

## 🔗 常用命令

```bash
# 显示详细输出
pytest -v

# 显示打印语句
pytest -s

# 在第一个失败处停止
pytest -x

# 显示最慢的10个测试
pytest --durations=10

# 并行运行测试
pytest -n auto
```

## 📖 文件说明

详见各文件内的详细注释和文档。

## 💡 最佳实践

1. **页面对象模型** - 将UI元素和交互逻辑分离
2. **显式等待** - 等待元素出现而不是固定延迟
3. **日志记录** - 记录每一步操作便于调试
4. **截图保存** - 失败时自动截图
5. **参数化测试** - 使用pytest.mark.parametrize减少代码重复
6. **基础类** - 提取通用功能到基础类

## 🎯 项目目标

通过学习本项目，你将掌握：
- Playwright自动化框架的使用
- API自动化测试的最佳实践
- pytest测试框架
- 测试报告生成
- CI/CD集成

祝学习愉快！ 🎉
