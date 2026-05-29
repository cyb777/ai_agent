#导入日志模块，用于输出日志
from app.utils.logger import Logger
#导入模型类
from app.ai.model.model import MyModel
from app.ai.tool.mysql_tool import mysql_tool
from app.ai.tool.send_email_tool import send_email
#导入邮箱响应格式,用于规范智能体返回的数据格式
from app.ai.schema.emailResponse import EmailResponse
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
#导入异步IO库，支持异步流式输出
import asyncio

#获取当前模块的日志对象，用于记录日志
logger = Logger.get_logger(__name__)
"""
sql问题智能体
功能：负责回答用户的sql问题

"""


class SQLQuestionAgent:
    def __init__(self):
        #打印日志
        logger.info("SQLQuestionAgent初始化")
        self.model = MyModel.get_model()
        self.tools = self.__init__tools()
        #初始化智能体方法，创建完整智能体
        self.agent = self.__init__agent()

    def __init__tools(self):
        self.tools = [mysql_tool]
        return self.tools

    def __init__agent(self):
        prompt = """
        一:你是一个sql问题智能体,你有一个工具mysql_tool
        二:重要规则：
            只能经行select查询，不能进行delete 操作
        三：使用规则：
            1.如果查询销售数据查询，请查询sales
            2.多表查询，请使用join
            3.不要回答你的思考过程
        """
        agent = create_agent(
            model=self.model,
            tools=self.tools,
            system_prompt=prompt,
            checkpointer=InMemorySaver(),
        )
        return agent

    #创建问题并异步流式回答
    async def create_question(self, question: str, user_id: str):
        response = self.agent.astream(
            # 传入用户问题
            {"messages": [{"role": "user", "content": question}]},
            {"configurable": {"thread_id": 10}},
            stream_mode="messages"
        )
        # 异步遍历流式响应
        async for c, m in response:
            yield c.content

    async def stream(self, question: str, user_id: str):
        async for text in self.create_question(question, user_id):
            #每一段内容都返回给前端
            yield {
                "text": text,  # 当前返回文本片段
                "done": False,  # 标记未结束
            }
        yield {
            "done": True
        }

    async def answer(self, question: str, user_id: str):
        # 异步遍历流式响应
        async for text in self.create_question(question, user_id):
            yield text
        yield ""