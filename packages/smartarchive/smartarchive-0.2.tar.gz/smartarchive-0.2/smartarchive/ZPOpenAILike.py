from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.llms.openai_like import OpenAILike
from llama_index.core import Settings
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core import SimpleDirectoryReader, SummaryIndex
from zhipuai import ZhipuAI
from typing import Any, List
from pydantic import Field
import os

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

documents = SimpleDirectoryReader("../data").load_data()
index = SummaryIndex.from_documents(documents)
query_engine = index.as_query_engine()
response = query_engine.query(
    "请用json的格式列出互联网数据分布式抓取平台技术服务合同的金额、名称、甲方、乙方、违约条款、合同期限")
print(response)



