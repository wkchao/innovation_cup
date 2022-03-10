import sqlite3


def db_init():
    crawler_data = sqlite3.connect('crawler_data.db')
    crawler_cursor = crawler_data.cursor()
    crawler_cursor.execute("DROP TABLE IF EXISTS PD_table")
    crawler_cursor.execute("""
                        CREATE TABLE PD_table (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          title TEXT NOT NULL,
                          content TEXT NOT NULL,
                          keyword TEXT NULL
                        )
                        """)
    crawler_cursor.execute("DROP TABLE IF EXISTS WB_table")
    crawler_cursor.execute("""
                        CREATE TABLE WB_table (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          createTime TEXT NOT NULL,
                          content TEXT NOT NULL,
                          keyword TEXT NULL
                        )
                        """)
    crawler_data.commit()
    crawler_cursor.close()
    crawler_data.close()


def WB_table_search(id):
    crawler_data = sqlite3.connect('crawler_data.db')
    crawler_cursor = crawler_data.cursor()
    sql_text = "SELECT * FROM WB_table WHERE id=" + id
    # print(sql_text)
    crawler_cursor.execute(sql_text)
    res = crawler_cursor.fetchone()
    crawler_data.commit()
    crawler_cursor.close()
    crawler_data.close()
    return res


def WB_table_insert(item):
    if item is None or item['text'] is None:  # 爬取结果为空或者过滤后文本为空
        return
    elif WB_table_search(item['id']) is not None:
        print(item['id'] + "已存在，跳过")
        return
    crawler_data = sqlite3.connect('crawler_data.db')
    crawler_cursor = crawler_data.cursor()
    sql_text = "INSERT INTO WB_table VALUES(" + item['id'] + ", '" + item['createTime'] + "', '" + item['text'] + "', '')"
    # print(sql_text)
    crawler_cursor.execute(sql_text)
    crawler_data.commit()
    crawler_cursor.close()
    crawler_data.close()
    print(item['id'] + "写入成功！")


def PD_table_insert(item):
    crawler_data = sqlite3.connect('crawler_data.db')
    crawler_cursor = crawler_data.cursor()
    sql_text = "INSERT INTO PD_table VALUES(" + item['id'] + ", '" + item['createTime'] + "', '" + item['text'] + "', '')"
    # print(sql_text)
    crawler_cursor.execute(sql_text)
    crawler_data.commit()
    crawler_cursor.close()
    crawler_data.close()


def WB_table_readall():
    crawler_data = sqlite3.connect('crawler_data.db')
    crawler_cursor = crawler_data.cursor()
    sql_text = "SELECT * FROM WB_table"
    # print(sql_text)
    crawler_cursor.execute(sql_text)
    res = crawler_cursor.fetchall()
    crawler_data.commit()
    crawler_cursor.close()
    crawler_data.close()
    return res


if __name__ == '__main__':
    db_init()
