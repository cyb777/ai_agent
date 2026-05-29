# 基于 LLM 智能体的自然语言数据分析与可视化平台

## 项目简介

基于 FastAPI + LangChain 的智能数据分析平台，集成阿里云通义千问 Qwen3-max 大模型，通过自然语言驱动数据库查询、图表生成和数据分析。

### 核心功能

- **自然语言转 SQL**：SQLQuestionAgent 流式输出查询结果
- **数据可视化**：EchartsAgent 自动生成 ECharts 图表
- **智能分析**：AnlyzeAgent 三步流程（查询→分析→图表）
- **登录验证**：SystemAgent 双工具协作完成邮箱验证码登录

## 技术栈

| 层面 | 技术 |
|------|------|
| 后端框架 | FastAPI |
| 智能体框架 | LangChain + LangGraph |
| 大模型 | 阿里云通义千问 Qwen3-max |
| 数据库 | MySQL + Redis |
| 前端 | Vue.js + ECharts |

## 项目结构

```
ai_agent/
├── app/
│   ├── main.py                  # FastAPI 入口，生命周期管理
│   ├── ai/
│   │   ├── agent/
│   │   │   ├── system_agent.py      # 登录验证码智能体
│   │   │   ├── sql_question_agent.py # SQL 问答智能体
│   │   │   ├── echarts_agent.py      # 图表生成智能体
│   │   │   └── anlyze_agent.py       # 数据分析智能体
│   │   ├── tool/
│   │   │   ├── mysql_tool.py         # MySQL 查询工具
│   │   │   └── send_email_tool.py    # 邮件发送工具
│   │   ├── model/
│   │   │   └── model.py             # 模型单例管理
│   │   └── schema/                   # Pydantic 数据模型
│   ├── api/
│   │   ├── chat/                     # 聊天路由
│   │   └── system/                   # 系统路由（登录/注册）
│   └── utils/
│       └── logger.py                 # 日志工具类
├── requirements.txt
├── .env.example                      # 环境变量模板
└── README.md
```

## 快速开始

### 1. 环境配置

```bash
# 克隆项目
git clone <your-repo-url>
cd ai_agent

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入你的 API Key 和数据库配置
```

### 2. 启动服务

```bash
python app/main.py
# 或
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. 访问

- API 文档：http://localhost:8000/docs
- 聊天接口：GET /chat?question=你的问题&user_id=1
