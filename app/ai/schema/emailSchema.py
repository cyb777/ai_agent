from pydantic import BaseModel,Field

# 定义一个邮件工具的参数
class EmailSchema(BaseModel):
    #...表示必须要传递的参数
    to: str = Field(..., description="收件人邮箱地址")
    subject: str = Field(..., description="邮件主题")
    content: str = Field(..., description="邮件内容")