#导入FASTAPI的核心类，用于创建web应用
from fastapi import FastAPI

from app.ai.agent.echarts_agent import EchartsAgent
#导入日志
from app.utils.logger import Logger
from app.ai.agent.system_agent import SystemAgent
from app.ai.agent.sql_question_agent import SQLQuestionAgent
from app.ai.agent.anlyze_agent import AnlyzeAgent
#导入异步上下文管理
from contextlib import asynccontextmanager
#导入跨域中间件
from fastapi.middleware.cors import CORSMiddleware
#相关接口
from app.api.system.system_router import system_router
from app.api.chat.chat_router import chat_router

#获取当前模块的日志对象，用于记录日志
logger = Logger.get_logger(__name__)


#定义服务生命周期，服务启动时创建智能体实例，服务停止时销毁智能体实例
@asynccontextmanager
async def lifespan(app: FastAPI):
    #  服务启动时：创建智能体实例，挂载到Fastapi的应用状态
    app.state.system_agent = SystemAgent()
    app.state.sql_question_agent = SQLQuestionAgent()
    app.state.echarts_agent = EchartsAgent()
    app.state.anlyze_agent = AnlyzeAgent()

    logger.info("登录智能体初始化完成")
    logger.info("sql问题智能体初始化完成")
    logger.info("echarts智能体初始化完成")
    logger.info("数据分析智能体初始化完成")
    yield
    # 服务停止时：销毁智能体实例
    logger.info("登录智能体销毁完成")
    logger.info("sql问题智能体销毁完成")
    logger.info("echarts智能体销毁完成")
    logger.info("数据分析智能体销毁完成")

app = FastAPI(lifespan=lifespan)

#添加跨域中间件，允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8081"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#注册系统路由，将system_router路由
app.include_router(system_router)
#注册聊天路由
app.include_router(chat_router)


if __name__ == "__main__":
    #导入系统模块
    import sys

    #构造启动命令
    cmd = [
        sys.executable, "-m", "uvicorn",
        "app.main:app",  #指定FastAPI应用设置
        "--host", "0.0.0.0",  #指定监听地址和端口
        "--port", "8000",
        "--reload"  #开启热重载
    ]
    #导入子进程模块
    import subprocess

    #启动子进程
    subprocess.run(cmd)
