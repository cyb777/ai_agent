from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()
class MyModel:
    _model = None
    @staticmethod
    def get_model():
        if MyModel._model is None:
            MyModel._model = ChatOpenAI(model=os.getenv('MODEL_NAME'),streaming=True)
        return MyModel._model