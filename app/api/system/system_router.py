from fastapi import APIRouter, Request
from app.api.schema.login_schema import LoginSchema, SendCodeSchema,RegisterCodeSchema,RegisterSchema
from app.utils.logger import Logger
import redis
from app.ai.tool.mysql_tool import mysql_tool
import random

# 创建redis连接
redis_conn = redis.Redis(host="127.0.0.1", port=6379, db=0)

# 加载日志
logger = Logger.get_logger(__name__)
# 创建路由器
system_router = APIRouter()


# 登录发送验证码参数接口
@system_router.post("/send_code")
def send_code(request: Request, args: SendCodeSchema):
    agent = request.app.state.system_agent
    rs = agent.answer(args.email)
    # 登录专用 Key
    redis_conn.set(f"login:code:{args.email}", rs["data"], ex=60)
    logger.info(f"登录验证码发送成功")
    return {"code": rs["code"], "msg": rs["msg"]}

# 登录参数接口
@system_router.post("/login")
def login(args: LoginSchema):
    try:
        redis_key = f"login:code:{args.email}"
        code_bytes = redis_conn.get(redis_key)
        if code_bytes and code_bytes.decode() == args.code:
            logger.info(f"登录验证码正确")
            return {"code": 200, "msg": "登录成功"}
        else:
            return {"code": 500, "msg": "验证码错误或已过期"}
    except Exception as e:
        logger.error(f"登录异常：{e}")
        return {"code": 500, "msg": "登录失败"}


# 注册发送验证码参数接口
@system_router.post("/register_send_code")
def register_send_code(request: Request, args: RegisterCodeSchema):
    if "@" not in args.email:
        return {"code": 400, "msg": "请输入正确的邮箱格式"}

    verify_code = str(random.randint(100000, 999999))

    #
    redis_key = f"reg:code:{args.email}"
    redis_conn.set(redis_key, verify_code, ex=60)

    agent = request.app.state.system_agent
    task_prompt = f"用户正在注册，请调用邮件工具向 {args.email} 发送验证码：{verify_code}"

    try:
        agent.answer(task_prompt)
        logger.info(f"注册验证码已发送：{args.email}, code: {verify_code}")
        return {"code": 200, "msg": "验证码已发送至邮箱"}
    except Exception as e:
        logger.error(f"Agent 发送失败: {e}")
        return {"code": 500, "msg": "邮件服务异常"}

# 注册参数接口
@system_router.post("/register")
def register(args: RegisterSchema):
    try:
        # 1. 验证 Key 和验证码 (确保 Key 为 reg:code:{email})
        redis_key = f"reg:code:{args.email}"
        redis_code = redis_conn.get(redis_key)

        if redis_code is None:
            return {"code": 500, "msg": "验证码已过期，请重新获取"}

        if redis_code.decode() != str(args.code):
            return {"code": 500, "msg": "验证码错误"}

        # 2. 查询用户是否存在
        sql = f"SELECT * FROM email WHERE email='{args.email}'"

        # 【核心修改】：使用 .run() 来调用被 @tool 装饰的对象
        result = mysql_tool.run(sql)

        if result and result != "()" and result != "[]" and "数据库操作失败" not in result:
            return {"code": 500, "msg": "用户已注册"}

        # 3. 执行注册
        insert_sql = f"INSERT INTO email(user_name, email) VALUES('user', '{args.email}')"

        # 【核心修改】：同理使用 .run()
        insert_result = mysql_tool.run(insert_sql)

        logger.info(f"注册写入结果: {insert_result}")

        # 4. 成功后删除验证码
        redis_conn.delete(redis_key)
        return {"code": 200, "msg": "注册成功"}

    except Exception as e:
        logger.error(f"注册接口异常: {e}")
        return {"code": 500, "msg": "注册失败"}







