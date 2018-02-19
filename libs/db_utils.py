import os
from datetime import datetime
import sqlite3 as sql

base_path = "./DB/"

# DBに書き込み
def write_memo(channel, title, detail):
    path = base_path + channel + ".db"
    if os.path.exists(path):
        conn = sql.connect(path)
    else:
        conn = sql.connect(path)
        conn.execute("create table list (id integer, title text, detail text)")
        conn.commit()
    SQL = "insert into list values(?,?,?)"
    value = (int(datetime.now().timestamp()), title, detail)
    conn.execute(SQL, value)
    conn.commit()
    conn.close()

# DBから削除
def del_memo(channel, title):
    path = base_path + channel + ".db"
    if os.path.exists(path):
        conn = sql.connect(path)
    else:
        return
    conn.row_factory = sql.Row
    cur = conn.cursor()
    conn.execute("delete from list where title = ?",(title,))
    conn.commit()
    conn.close()

# DB更新
def update_memo(channel, title, detail):
    del_memo(channel, title)
    write_memo(channel, title, detail)

# DBからリスト取得
def get_list(channel):
    path = base_path + channel + ".db"
    titlelist = []
    if os.path.exists(path):
        conn = sql.connect(path)
    else:
        return titlelist
    conn.row_factory = sql.Row
    cur = conn.cursor()
    cur.execute( "select * from list order by id desc" )
    for row in cur:
        titlelist.append(row["title"])
    cur.close()
    conn.close()
    return titlelist

# DBから詳細情報取得
def get_detail(channel, title):
    path = base_path + channel + ".db"
    if os.path.exists(path):
        conn = sql.connect(path)
    else:
        return None
    conn.row_factory = sql.Row
    cur = conn.cursor()
    try:
        cur.execute("select * from list where title = ?",(title,))
        row = cur.fetchone()
        detail = {
            "title":row["title"],
            "detail":row["detail"]
        }
    except:
        detail = None
    cur.close()
    conn.close()
    return detail