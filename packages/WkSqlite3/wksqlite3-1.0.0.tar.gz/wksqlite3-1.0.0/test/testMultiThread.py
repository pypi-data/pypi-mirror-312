from threading import Thread
import time
from WkSqlite3 import WkSqlite3

db = WkSqlite3("test.db")
TABLE1 = "test1"
TABLE2 = "test2"
db.set_table(TABLE1).create_table(
    {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "name": "TEXT",
        "age": "INTEGER",
        "sex": "INTEGER",
    }
)
db.set_table(TABLE2).create_table(
    {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "name": "TEXT",
        "age": "INTEGER",
        "sex": "INTEGER",
    }
)


def f(name, table_name):
    for i in range(1):
        # db.set_table(table_name).insert_row({"name": f"{name}_{i}"})
        # print(db.set_table(table_name).select_one({"id": 1}))
        # db.set_table(table_name).select_one({"id": 1000})
        db.set_table(table_name).select_all()
        db.set_table(table_name).select(id=100)
        db.set_table(table_name).select(id1=100)
        


if __name__ == "__main__":
    start = time.time()
    # 1000 18.64120316505432 single
    # 1000 33.692219257354736 multi
    f(f"thread_{0}", TABLE1)

    threads: list[Thread] = []
    for i in range(200):
        threads.append(Thread(target=f, args=(f"thread_{i}", TABLE1 if i == 0 else TABLE2)))

    for t in threads:
        t.start()
    for t in threads:
        t.join()
    end = time.time()
    print(end - start)
