# DeepSeek 流式对话网页助手
> 基于 Streamlit + DeepSeek API 实现的轻量化网页聊天项目，模块化设计，适合演示

## ✨ 功能
- 网页端交互式对话
- Temperature 参数调节，控制回答随机性
- 对话记录导出为 Markdown
- 上下文截断，防止上下文无限膨胀、避免高额 API 消耗
- 调用日志打印，实时查看每一次请求的 Token 用量与预估开销
- 支持一键切换 `deepseek-chat` / `deepseek-flash` 模型

## 📁 项目结构
- `main.py`：程序入口、网页界面
- `api_client.py`：封装 API 请求逻辑
- `utils.py`：工具函数，Token 估算、上下文截断
- `.env.example`：密钥配置模板
- `.gitignore`：屏蔽敏感文件（.env）

## 🚀 运行方式
```bash
pip install -r requirements.txt
streamlit run main.py