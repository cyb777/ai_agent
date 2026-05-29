from langchain.tools import tool
from app.ai.schema.emailSchema import EmailSchema
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
from app.utils.logger import Logger

# 加载日志
logger = Logger.get_logger(__name__)

# 加载环境变量文件
load_dotenv()
# 定义一个智能体工具
@tool("send_emai",args_schema=EmailSchema)
def send_email(to:str,subject:str,content:str)-> str:
    """
    发送邮件
    """
    try:
        # 创建一个邮件对象
        msg = MIMEText(content)
        # 设置收件人
        msg['to'] = to
        msg['from'] = os.getenv("EMAIL_FROM")
        # 设置邮件主题
        msg['subject'] = subject
        # 创建一个SMTP对象
        smtp = smtplib.SMTP_SSL(os.getenv('EMAIL_HOST'), 465)
        # 登录邮箱
        smtp.login(os.getenv('EMAIL_FROM'), os.getenv("EMAIL_PASSWORD"))
        # 发送邮件
        smtp.sendmail(msg['from'], msg['to'], msg.as_string())
        logger.info("邮件发送成功")
        return "邮件发送成功"
    except Exception as e:
        logger.error("邮件发送失败")
        return "邮件发送失败"
