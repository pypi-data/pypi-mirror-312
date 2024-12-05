from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.llms.openai_like import OpenAILike
from llama_index.core import Settings
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core import SimpleDirectoryReader, SummaryIndex
from zhipuai import ZhipuAI
from typing import Any, List
from pydantic import Field
import os
from llama_index.core.tools import FunctionTool, QueryEngineTool
from llama_index.llms.openai import OpenAI
from llama_index.core.agent import ReActAgent

api_key = "01d2e542d5c8192cc1f5be1138cd3a72.NcbuwvFpbE8kycTu"
api_base = "https://open.bigmodel.cn/api/paas/v4"
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


Settings.llm = llm
Settings.embed_model = ZhipuEmbeddings()

os.environ["TOKENIZERS_PARALLELISM"] = "false"




# define sample Tool

documents = SimpleDirectoryReader("../data").load_data()
index = SummaryIndex.from_documents(documents)
query_engine = index.as_query_engine()

my_query_tool = QueryEngineTool.from_defaults(
    query_engine,
    name="技术开发合同",
    description="技术开发合同的基本信息",
)
def Approval_status(
        contract: str =Field(
            description="合同的名称"
        ),
        oper_type: str =Field(
            description="业务类型，比如审核、付款等"
        ),
) -> str:
    """用于查询合同业务审批或付款情况"""
    print("获得参数contract:"+contract+ " 业务类型:"+ oper_type)
    return "已完成审批"


def contract_sum(begin: str,  end: str) -> str:
    """用于统计指定的起始时间到截止时间的合同金额"""
    print("获得参数begin:"+begin+"  end:"+end)
    return {"ret:'success',data:'100'"}


def current_year(begin: str) -> str:
    """用于将'今年'转变成当前时间"""
    print("获得参数begin:"+begin)
    return "2024年1月1到2024年12月31日"




contract_sum = FunctionTool.from_defaults(fn=contract_sum)

current_year = FunctionTool.from_defaults(fn=current_year)

Approval_status = FunctionTool.from_defaults(fn=Approval_status)


# initialize ReAct agent
agent = ReActAgent.from_tools([current_year, contract_sum, Approval_status, my_query_tool], llm=llm, verbose=True)

response = agent.chat("维保合同的审批情况怎么样了")
print(response)

#response = agent.chat("技术开发合同的甲方是谁")
#print(response)


