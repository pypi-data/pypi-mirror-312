from WkSqlite3 import WkSqlite3

db = WkSqlite3("test.db")
db.set_table("tmp1111").create_table(
    {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "key": "TEXT",
        "sno": "TEXT",
        "role": "TEXT",
    },
    delete_if_exists=True,
)
