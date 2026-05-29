from pydantic import BaseModel,Field

class mysqlSchema(BaseModel):
    sql: str = Field(..., description="mysql语句")