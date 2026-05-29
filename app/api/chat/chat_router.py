import json
from fastapi import APIRouter, Request
from app.utils.logger import Logger
from fastapi.responses import StreamingResponse

# 加载日志
logger = Logger.get_logger(__name__)

# 创建聊天路由
chat_router = APIRouter()


# 创建聊天接口
@chat_router.get("/chat")
async def chat(request: Request, question: str, user_id: str):
    # 根据用户问题路由到对应智能体
    if "图表" in question:
        # 图表智能体
        echarts_agent = request.app.state.echarts_agent
        return echarts_agent.answer(question, user_id)

    elif "数据分析" in question:
        # 数据分析智能体
        anlyze_agent = request.app.state.anlyze_agent
        data = anlyze_agent.answer(question, user_id)
        return {"code": 200, "data": data}

    # 默认：普通 SQL 问答智能体（内存级）
    current_use_agent = request.app.state.sql_question_agent

    # 流式返回逻辑
    async def generator():
        try:
            method = getattr(current_use_agent, "answer", None)

            if not method:
                yield f"data:{json.dumps({'content': '智能体方法不存在', 'done': True}, ensure_ascii=False)}\n\n"
                return

            # 流式输出
            async for chunk in method(question, user_id):
                msg = {"content": chunk, "done": False}
                yield f"data:{json.dumps(msg, ensure_ascii=False)}\n\n"

            # 结束标识
            msg = {"content": "", "done": True}
            yield f"data:{json.dumps(msg, ensure_ascii=False)}\n\n"

        except Exception as e:
            logger.error(f"流式返回错误：{str(e)}")
            yield f"data:{json.dumps({'content': '服务出错', 'done': True, 'error': True}, ensure_ascii=False)}\n\n"

    return StreamingResponse(content=generator(), media_type="text/event-stream")