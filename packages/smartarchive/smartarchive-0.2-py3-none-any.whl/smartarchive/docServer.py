from flask import Flask, request, render_template
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, SummaryIndex
import chromadb
import uuid
import multiprocessing

#os.environ['OPENAI_API_KEY'] = "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"

#智普
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.llms.openai_like import OpenAILike
from llama_index.core import Settings
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core import SimpleDirectoryReader, SummaryIndex
from zhipuai import ZhipuAI
from typing import Any, List
from pydantic import Field
import os
from datetime import datetime


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

app = Flask(__name__)

base_dir = "/root/ai_doc/upload"
save_collection = "project-collection"
chroma_store_path = "./chroma_store_new11"

@app.route('/uploadAndLearn', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        format = request.form['format']
        tmp_dir = base_dir + "/" + str(uuid.uuid4())
        os.makedirs(tmp_dir)
        fpath = os.path.join(tmp_dir, f.filename)
        f.save(fpath)
        return multiprocessDigiest(tmp_dir, format)

@app.route('/uploadToVectorStore', methods=['GET', 'POST'])
def vectorStore():
    if request.method == 'POST':
        f = request.files['file']
        project_id = request.form['projectId']
        doc_id = request.form['docId']
        project_name = request.form['projectName']
        tmp_dir = base_dir + "/" + str(uuid.uuid4())
        os.makedirs(tmp_dir)
        fpath = os.path.join(tmp_dir, f.filename)
        f.save(fpath)
        store2db(tmp_dir, doc_id, project_id, project_name)
        respDict = dict(code=200, msg="success")
        print(respDict)
        return respDict

def digiest(data_dir, format):
    docs = SimpleDirectoryReader(data_dir).load_data()
    index = SummaryIndex.from_documents(docs)
    query_engine = index.as_query_engine(response_mode="compact")
    response = query_engine.query("请用标准的json格式列出合同的名称、内容、金额、甲方、乙方、违约条款、合同开始时间（标准时间格式）、合同结束时间（标准时间格式）、委托方联系人、委托方联系方式、委托方通讯地址") if format == 'json' \
        else query_engine.query("请列出合同的名称、金额、甲方、乙方、违约条款、合同开始时间（标准时间格式）、合同结束时间（标准时间格式）、内容、委托方联系人、委托方联系方式、委托方通讯地址，输出每一项结果，以换行分割,禁止空白行")
    print(response)
    return response.response

def multiprocessDigiest(data_dir, format):
    manager = multiprocessing.Manager()
    shared_dic = manager.dict()
    questions = ["合同的委托方是谁,请不要回答其他内容。举例如下： {'contractPartyA':'字节跳动'}",
                 "合同的名称是什么,请不要回答其他内容。举例如下： {'contractName':'开发委托合同'}",
                 "合同的被委托方是谁,请不要回答其他内容。举例如下： {'contractPartyB':'腾讯集团'}",
                 "合同的金额是多少,请不要回答其他内容。举例如下： {'amount':200}",
                 "合同的违约条款是什么,请不要回答其他内容。举例如下： {'defaultClause':'需支付违约金100万元'}",
                 "合同的服务内容是什么,请不要回答其他内容。举例如下： {'contractContent':'内容包含移动端等开发设计'}",
                 "合同履行的起始结束时间是什么,请不要回答其他内容。举例如下： {'start': '2024-10-11', 'end':'2024-10-30'}",
                 "合同的委托方联系人是谁,请不要回答其他内容。举例如下： {'contactPerson':'张三'}",
                 "合同委托方联系电话是什么,请不要回答其他内容。举例如下： {'phone':'18566665656'}",
                 "合同委托方通讯地址是什么,请不要回答其他内容。举例如下： {'address':'广州天河岗顶302号'}",
                 "合同付款方式是什么,如果分多次付款，按期数，付款金额，应付时间，分别列出，请不要回答其他内容。举例如下： {'paymentMethod':[{'period': '1', 'amount':'20000', 'deadline': '2024-10-29 00:00:00'}]}",
                 "合同委托方邮箱是什么,请不要回答其他内容。举例如下： {'email':''}"]
    processes = []
    for question in questions:
        process = multiprocessing.Process(target=useAI, args=(data_dir, question, shared_dic))
        processes.append(process)
    for process in processes:
        process.start()
    for process in processes:
        process.join()

    print("所有进程执行完毕")
    print(str(shared_dic))
    return str(shared_dic)

def useAI(data_dir,question, shared_dic):
    docs = SimpleDirectoryReader(data_dir).load_data()
    index = SummaryIndex.from_documents(docs)
    query_engine = index.as_query_engine()
    response = query_engine.query(question)
    print(response.response)
    #shared_dic[question] = response.response
    tempDict = eval(response.response)
    shared_dic.update(tempDict)
    #print("----------" + question +  ":\n" + shared_dic[question])


@app.route('/deleteFile', methods=['GET', 'POST'])
def deleteFile():
    if request.method == 'POST':
        doc_ids = request.form['docIds']
        idlist = doc_ids.split(",")
        for doc_id in idlist:
            client = chromadb.PersistentClient(path=chroma_store_path)
            # create collection
            chroma_collection = client.get_or_create_collection(save_collection)
            # assign chroma as the vector_store to the context
            vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
            storage_context = StorageContext.from_defaults(vector_store=vector_store)
            index = VectorStoreIndex.from_vector_store(vector_store=vector_store, storage_context=storage_context)
            index.delete_ref_doc(doc_id, delete_from_docstore=True)
        respDict = dict(code=200, msg="success")
        return respDict


def store2db(data_dir, doc_id, project_id, project_name):
    client = chromadb.PersistentClient(path=chroma_store_path)
    # create collection
    chroma_collection = client.get_or_create_collection(save_collection)
    # assign chroma as the vector_store to the context
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex.from_vector_store(vector_store=vector_store, storage_context=storage_context)

    docs = SimpleDirectoryReader(data_dir).load_data()

    docs[0].id_ = doc_id
    print(docs[0].id_)


    current_time = datetime.now()  # 获取当前时间
    current_time_str = current_time.strftime("%Y-%m-%d")  # 格式化时间为字符串
    print(current_time_str)
    docs[0].metadata = {"project": project_id, "project_name": project_name, "date": current_time_str}

    parser = SimpleNodeParser.from_defaults(chunk_size=1024, chunk_overlap=32)
    nodes = parser.get_nodes_from_documents(docs)
    index.insert_nodes(nodes)




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=18082)
