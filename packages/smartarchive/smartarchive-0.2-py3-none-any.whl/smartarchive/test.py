from flask import Flask, request ,render_template
from SqlUtil import execute_sql

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@app.route('/msg', methods=['GET', 'POST'])
def msg():
    return "SUCCESS"

print(execute_sql("select * from sys_user"))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


