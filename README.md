# DeepSeek 对话 Demo
> 基于 Streamlit + DeepSeek API 搭建的网页版大模型对话应用，适合入门学习，可部署上线。

## ✨ 功能
- ✅ 流式输出，文字逐字展示
- ✅ 侧边栏调节 Temperature、最大输出 Token
- ✅ 一键清空对话
- ✅ 上下文滑动窗口：只保留最近 4 轮对话，控制 Token 消耗
- ✅ 请求超时捕获，异常友好提示

## 🛠 环境依赖
```bash
pip install streamlit openai
