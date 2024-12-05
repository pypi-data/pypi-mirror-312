# llm
使用chroma向量数据库来存储内容，然后通过llamaindex框架进行问答

通过chroma的不同collection来区分内容数据，以便在检索时不会干扰

比如我有两个合同，每个合同及其相关资料存放在一个独立的collection中

使用flask作为快速构建RestFul接口

# python环境 3.11

windows 本地建议安装conda

linux 环境建议安装miniconda

如果在国内可以使用  清华智普作为大模型  目前配置了一个智普的key，可以自行申请 
如果在东京的服务器上可以用 openai的 key


开发环境建议使用pycharm 社区版
pycharm创建工程时可以指定使用conda提供的环境
conda windows安装请百度一下

pyhton 下如果确实package 可以使用 pip install 包名

# conda的常用命令
conda create -n myenv python=3.11   创建一个名字叫做myenv的环境，python使用3.11
conda activate myenv   将当前python环境切换到  myenv这个环境
conda list env   列出当前有那些环境
conda env list  列出当前环境下有哪些package

# 项目作为依赖库使用
pip install path/to/youlib/dist/smartarchive-0.1.tar.gz
