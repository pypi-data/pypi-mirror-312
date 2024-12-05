import pymysql


def get_db():
    """
    获取数据库连接对象
    """
    # 打开数据库连接
    db = pymysql.connect(
        host="47.91.24.169", port=3306, user="root", passwd="bjzy@2024", db="dms"
    )
    return db


def get_sql_conn():
    """
    获取数据库连接和游标对象
    """
    db = get_db()
    cursor = db.cursor()
    return db, cursor

def execute_sql(sql):
    db = get_db()
    cursor = db.cursor()

    # 执行查询
    cursor.execute(sql)

    # 获取所有结果
    rows = cursor.fetchall()

    # 将结果转换为字典列表
    results = [dict(zip(tuple(column[0] for column in cursor.description), row)) for row in rows]

    # 关闭游标和连接
    cursor.close()
    db.close()
    return results







