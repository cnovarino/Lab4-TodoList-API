import sqlite3

DB_PATH = './todo_restfull.db'

def start_db():
    conn = sqlite3.connect(DB_PATH)
    CREATE_SQL = '''CREATE TABLE IF NOT EXISTS "items"  (
            "id" INTEGER PRIMARY KEY,
            "todo" TEXT NOT NULL,
            "completed" INTEGER NOT NULL DEFAULT 0
        );'''
    c = conn.cursor()
    c.execute(CREATE_SQL)
    conn.commit()


def add_to_list(task):
    print(task)
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('INSERT INTO items(todo) values(?)', (task,))
        conn.commit()
        return {"todo": task}
    except Exception as e:
        print('Error: ', e)
        return None


todo_list = {}


def get_all_items():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('select * from items')
        rows = c.fetchall()
        return rows
    except Exception as e:
        print('Error: ', e)
        return None


def get_item(item_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("select * from items where id='%s'" % item_id)
        item = c.fetchone()
        if item:
            return {'todo': item}
        return None
    except Exception as e:
        print('Error: ', e)
        return None


def update_status(item_id, status):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('update items set completed=? where id=?', (status, item_id))
        conn.commit()
        return True
    except Exception as e:
        print('Error: ', e)
        return None


def delete_item(item_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('delete from items where id=?', item_id)
        conn.commit()
        return {'delete': 1}
    except Exception as e:
        print('Error: ', e)
        return None