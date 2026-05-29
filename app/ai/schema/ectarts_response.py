from pydantic import BaseModel, Field


#定义一个类作为输出格式
class EchartsResponse(BaseModel):
    data:str = Field(...,description="json数据")
    code: int = Field(..., description="状态码")
    msg: str = Field(..., description="提示信息")