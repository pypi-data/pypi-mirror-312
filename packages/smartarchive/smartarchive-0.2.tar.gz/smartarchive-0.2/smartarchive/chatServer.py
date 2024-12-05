
from flask import Flask, request
from llama_index.core.agent import ReActAgent
from llama_index.core.base.llms.types import ChatMessage
from llama_index.core.chat_engine.types import ChatMode
from llama_index.core.tools import QueryEngineTool
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
from llama_index.core import StorageContext

#智普
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.llms.openai_like import OpenAILike
from llama_index.core import VectorStoreIndex, Settings
from zhipuai import ZhipuAI
from typing import Any, List
from pydantic import Field
import os

import importlib.abc
import importlib.util


from llama_index.core.vector_stores import (
    MetadataFilter,
    MetadataFilters,
)

api_key = "01d2e542d5c8192cc1f5be1138cd3a72.NcbuwvFpbE8kycTu"
api_base = "https://open.bigmodel.cn/api/paas/v4"
model = "glm-4"
llm = OpenAILike(
    model=model,
    api_base=api_base,
    api_key=api_key,
    is_chat_model=True,
    is_local=False,
    is_function_calling_model=False,
)



class FileLoader(importlib.abc.Loader):
    def __init__(self, file_path):
        self.file_path = file_path

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        exec(code, module.__dict__)

def load_module_from_file(module_name, file_path):
    loader = FileLoader(file_path)
    spec = importlib.util.spec_from_file_location(module_name, file_path, loader=loader)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module




class ZhipuEmbeddings(BaseEmbedding):
    client: ZhipuAI = Field(default_factory=lambda: ZhipuAI(api_key=api_key))

    def __init__(
            self,
            model_name: str = "embedding-3",
            **kwargs: Any,
    ) -> None:
        super().__init__(model_name=model_name, **kwargs)
        self.model_name = model_name

    def invoke_embedding(self, query: str) -> List[float]:
        response = self.client.embeddings.create(
            model=self.model_name, input=[query], dimensions=256
        )

        # 检查响应是否成功
        if response.data and len(response.data) > 0:
            return response.data[0].embedding
        else:
            raise ValueError("Failed to get embedding from ZhipuAI API")

    def _get_query_embedding(self, query: str) -> List[float]:
        return self.invoke_embedding(query)

    def _get_text_embedding(self, text: str) -> List[float]:
        return self.invoke_embedding(text)

    def _get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        return [self._get_text_embedding(text) for text in texts]

    async def _aget_query_embedding(self, query: str) -> List[float]:
        return self._get_query_embedding(query)

    async def _aget_text_embedding(self, text: str) -> List[float]:
        return self._get_text_embedding(text)

    async def _aget_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        return self._get_text_embeddings(texts)

#os.environ['OPENAI_API_KEY'] = "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"
#llm = OpenAI(model="gpt-4o")
Settings.llm = llm
Settings.embed_model = ZhipuEmbeddings()

os.environ["TOKENIZERS_PARALLELISM"] = "false"

app = Flask(__name__)

save_collection = "project-collection"
chroma_store_path = "./chroma_store_new11"
tool_error_msg = "```python\ntool_call("
module_path = "/home/plugins/ToolPlugin.py"
#module_path = "F:\plugins\ToolPlugin.py"
module_name = "ToolPlugin"
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    json = request.get_json()
    text = json['msg']
    project_id = None
    history = None
    if 'history' in json:
        history = json['history']
    if 'project_id' in json:
        project_id = json['project_id']
    return response(text, history, project_id)

def init_query_engine(project_id):
    index = getIndex()
    filters = MetadataFilters(
        filters=[
            MetadataFilter(key="project", value=project_id),
        ],
    )
    query_engine = index.as_query_engine(similarity_top_k=5, filters=filters if project_id is not None else None, response_mode='tree_summarize')
    return query_engine

def init_chat_engine(project_id):
    index = getIndex()
    filters = MetadataFilters(
        filters=[
            MetadataFilter(key="project", value=project_id),
        ],
    )
    from llama_index.core.memory import ChatMemoryBuffer
    memory = ChatMemoryBuffer.from_defaults(token_limit=3900)
    chat_engine = index.as_chat_engine(
        chat_mode=ChatMode.CONDENSE_PLUS_CONTEXT,
        memory=memory,
        llm=llm,
        filters=filters if project_id is not None else None,
        context_prompt=(
            "You are a chatbot, able to have normal interactions, as well as talk"
            " about an essay discussing contract information."
            "Here are the relevant documents for the context:\n"
            "{context_str}"
            "\nInstruction: Use the previous chat history, or the context above, to interact and help the user."
        ),
        verbose=True,
    )
    return chat_engine


def response(msg, history, project_id):
    query_engine = init_query_engine(project_id)
    chat_history = []
    for item in history:
        chat_history.append(ChatMessage(
            role="user",
            content=item
        ))
    chat_history.append(ChatMessage(content = "以上是历史聊天消息", role="user"))

    doc_tool = QueryEngineTool.from_defaults(
        query_engine,
        name="doc",
        description="用于查询合同的基本信息",
    )

    plugin_module = load_module_from_file(module_name, module_path)
    function_tools = plugin_module.function_tool_list()
    function_tools.append(doc_tool)
    agent = ReActAgent.from_tools(function_tools, llm=llm, verbose=True)
    question = "尝试使用工具然后中文回答这个问题：" + msg
    res = agent.chat(message=question, chat_history= chat_history)
    print(res.response)
    agent.reset()
    if tool_error_msg in res.response:
        res = agent.chat(message=question)
        print(res.response)
        if tool_error_msg in res.response:
            chat_engine = init_chat_engine(project_id=project_id)
            res = chat_engine.chat(msg, chat_history=chat_history)
            print(res.response)

    return res.response



def getIndex():
    client = chromadb.PersistentClient(path=chroma_store_path)
    # create collection
    chroma_collection = client.get_or_create_collection(save_collection)
    # assign chroma as the vector_store to the context
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_vector_store(
        vector_store, storage_context=storage_context
    )
    return index



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=18081)
