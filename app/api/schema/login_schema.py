from pydantic import BaseModel,Field


"""
登录发送验证码接口的参数模型
"""
class SendCodeSchema(BaseModel):
    email: str = Field(..., example="邮箱")

"""
登录接口的参数模型
"""
class LoginSchema(BaseModel):
    email: str = Field(..., example="邮箱")
    code: str = Field(..., example="验证码")


"""
注册发送验证码接口的参数模型
"""
class RegisterCodeSchema(BaseModel):
    email: str = Field(..., example="邮箱")

"""
注册接口的参数模型
"""
class RegisterSchema(BaseModel):
    email: str = Field(..., example="邮箱")
    code: str = Field(..., example="验证码")


