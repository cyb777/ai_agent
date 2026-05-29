#导入日志模块，用于输出日志
from app.utils.logger import Logger
#导入模型类
from app.ai.model.model import MyModel
from app.ai.tool.mysql_tool import mysql_tool
from app.ai.tool.send_email_tool import send_email
#导入邮箱响应格式,用于规范智能体返回的数据格式
from app.ai.schema.emailResponse import EmailResponse
from langchain.agents import create_agent

#获取当前模块的日志对象，用于记录日志
logger = Logger.get_logger(__name__)

"""
登录验证码智能体
功能：负责验证用户邮箱是否注册，并发送四位验证码邮件
"""


class SystemAgent:
    def __init__(self):
        #打印日志
        logger.info("SystemAgent初始化")
        self.model = MyModel.get_model()
        self.tools = self.init_tools()
        #初始化智能体方法，创建完整智能体
        self.agent = self.init_agent()

    #初始化智能体工具列表
    def init_tools(self):
        self.tools = [mysql_tool, send_email]
        return self.tools

    def init_agent(self):
        #定义提示词
        prompt = """
        一:你是一个邮箱登录验证智能体,你有两个工具
            1.mysql_tool:用于执行sql查询
            2.send_email:用于发送四位验证码邮件
        二:你必须严格按照流程执行
            1.根据用户问题，调用mysql_tool查询 user_info 表，查询用户邮箱是否存在
            2.调用send_email发送邮件，内容是 一组随机生成的不规则的四位数验证码
        三:反馈信息
            1.如果 mysql_tool 工具 验证邮箱失败 ，返回状态码 500，验证码为0，提示信息 邮箱不存在
            2.如果 send_email 工具 发送邮件成功 ，返回状态码 200，提示信息 发送成功
            3.如果 send_email 工具 发送邮件失败 ，返回状态码 500，提示信息：失败原因说明
             
        """
        #创建智能体
        self.agent = create_agent(
            model=self.model,
            tools=self.tools,
            system_prompt=prompt,
            response_format=EmailResponse
        )
        return self.agent

    #智能体执行方法，接受用户问题，返回智能体执行结果
    def answer(self, question):
        rs = self.agent.invoke({"messages": [{"role": "user", "content": question}]})
        #从智能体返回的结果中提取结构化数据
        answer = rs["structured_response"].model_dump()
        logger.info(f"智能体执行结果:{answer}")
        return answer


if __name__ == '__main__':
    agent = SystemAgent()
    agent.answer("给张三发送验证码")
