from pydantic import BaseModel,Field

# 定义一个类作为输出格式
class EmailResponse(BaseModel):
    data:str=Field(...,description="验证码")
    code: str = Field(..., description="状态码")
    msg: str = Field(..., description="提示信息")