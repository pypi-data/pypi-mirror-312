from flask import Flask, request, render_template
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, SummaryIndex
import chromadb
import uuid
import os

os.environ['OPENAI_API_KEY'] = "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"

app = Flask(__name__)

base_dir = "/root/ai_doc/upload"


@app.route('/uploadAndLearn', methods=['GET', 'POST'])
def uploader():
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
        return "success"


@app.route('/deleteFile', methods=['GET', 'POST'])
def deleteFile():
    if request.method == 'POST':
        project_id = request.form['projectId']
        doc_id = request.form['docId']
        client = chromadb.PersistentClient(path="./chroma_store_new")
        # create collection
        chroma_collection = client.get_or_create_collection(project_id)
        # assign chroma as the vector_store to the context
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_vector_store(vector_store=vector_store, storage_context=storage_context)
        index.delete_ref_doc(doc_id, delete_from_docstore=True)
        return "success"


def store2db(data_dir, doc_id, project_id, project_name):
    client = chromadb.PersistentClient(path="./chroma_store_new")
    # create collection
    chroma_collection = client.get_or_create_collection(project_id)
    # assign chroma as the vector_store to the context
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex.from_vector_store(vector_store=vector_store, storage_context=storage_context)

    docs = SimpleDirectoryReader(data_dir).load_data()

    docs[0].doc_id = doc_id
    docs[0].metadata = {"project": project_id, "project_name": project_name}

    parser = SimpleNodeParser.from_defaults(chunk_size=1024, chunk_overlap=32)
    nodes = parser.get_nodes_from_documents(docs)
    index.insert_nodes(nodes)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=18081)
