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
from app.ai.schema.ectarts_response import EchartsResponse
from langchain_core.messages import HumanMessage

#获取当前模块的日志对象，用于记录日志
logger = Logger.get_logger(__name__)

class EchartsAgent:
    def __init__(self):
        logger.info("初始化ECharts图表智能体")
        #初始化模型
        self.model = MyModel.get_model()
        #调用私有方法，初始化工具列表
        self.tools = self.__init__tools()
        #初始化内存记忆组件
        self.memory =InMemorySaver()


    #私有方法
    def __init__tools(self):
       #工具列表，只包含MySQL工具
       self.tools = [mysql_tool]
       #返回工具列表，供智能体使用
       return self.tools
    def answer(self, question: str, user_id: list):
        #定义系统提示词
        prompt = """
        一:你是一个ECharts图表智能体,你有一个工具mysql_tool
        二:工作流程:请严格按照以下步骤执行
        1.如果用户提问图表生成，请先查询数据库，生成一个echarts图表，图表数据josn格式必须是以下要求
        2.返回的数据必须是一个可执行的json格式，其他文本信息不重要
        3.返回的图表需要具有保存功能
        三:重要规则
        1.sql查询规范
             - 只能使用select查询，不能delete操作
        2.查询原则
             - 当涉及到排名top时，必须用order by 和limit 
             - 多表查询时，必须使用join 
             - 只查询前5条数据
        """
    #创建智能体实例
        agent = create_agent(
            model=self.model,
            tools=self.tools,
            system_prompt=prompt,
            checkpointer=self.memory,
            response_format=EchartsResponse,
        )
        try:
            #调用智能体回答问题
            response = agent.invoke(
                {"messages": [{"role": "user", "content": question}]},
                {"configurable": {"thread_id": 10}},
            )
            data = response["structured_response"].model_dump()

            logger.info(f"用户回答问题:{data}")
            return data
        except Exception as e:
            logger.error(e)
            return e
