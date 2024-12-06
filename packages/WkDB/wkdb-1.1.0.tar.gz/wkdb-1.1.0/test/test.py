from WkDB import WkDB
import time

DB = "test.db"
TABLE = "test_table"
TABLE2 = "test_table2"
if __name__ == "__main__":
    db = WkDB(host="localhost", user="root", password="123456", database="myproject", db_type="mysql")
    res = db.set_table("test_table").select_all()
    print(res)
    # db = WkDB(database=DB, db_type="sqlite3")
    # db.set_table(TABLE).create_table({"id": "INTEGER PRIMARY KEY AUTOINCREMENT", "name": "TEXT", "age": "INTEGER", "key": "TEXT", "sno": "TEXT"}, delete_if_exists=False)
    # db.set_table(TABLE2).create_table({"id": "INTEGER PRIMARY KEY AUTOINCREMENT", "name": "TEXT", "age": "INTEGER", "sex": "INTEGER", "key": "TEXT", "sno": "TEXT"}, delete_if_exists=True)
    # print(db.set_table(TABLE).select(id=1))
    # print(db.set_table(TABLE).select_one(id=1))
    # print(db.set_table(TABLE2).select(id=1))
    # print(db.set_table(TABLE2).select_one(id=10))
    # print(db.set_table(TABLE2).select_all())
    # print(db.select_all())
    # print(db.set_table(TABLE).select_all())
    # print(db.select_all())
    # res = db.set_table(TABLE2).get_column_names()
    # print(res)
    # exit()
    # for i in range(10):
    #     db.insert_row({"id": i * 10, "name": str(i), "age": str(i)})
    # db.execute(" CREATE TABLE IF NOT EXISTS users (`id` INTEGER PRIMARY KEY AUTOINCREMENT, `name` TEXT, `age` INTEGER)")
    # db.set_table(TABLE).delete_table()
    # db.set_table(TABLE).create_table({"id": "INTEGER PRIMARY KEY AUTOINCREMENT", "key": "TEXT", "sno": "TEXT"}, delete_if_exists=True)

    # db.execute_many("INSERT INTO test_table2(`key`, sno) VALUES(?, ?)", [[1, "test"], [2, "test2"]])
    # db.execute_many("UPDATE test_table2 SET `key`=? WHERE sno=?", [[10, "test"], [30, "test2"]])
    # db.set_table(TABLE)
    # res = db.execute("UPDATE `test_table` SET `key`=? WHERE `sno`=?", [22, "0"])
    # print(res)
    # res = db.update({"id": 1111}, {"id": 1})
    # print(res)
    # print(db.select_all())
    # with db.get_cursor() as cursor:
    #     # 查询表的列信息
    #     cursor.execute(f"PRAGMA table_info({TABLE})")

    #     # 获取列名
    #     columns = [column[1] for column in cursor.fetchall()]

    #     # 打印列名
    #     print(columns)
    # print(db.select_one(id="31"))
    # print(db.select_one(key="10"))
    """exists/exists_by_obj"""
    # db.set_table(TABLE)
    # print(db.set_table("gym_reserve").get_column_names())
    # print(db.exists(key="tQ0gK2eM4fR2uD1xK"))
    # print(db.exists(key="tQ0gK2eM4fR2uD1xK1"))
    # print(db.exists(sno=None))
    # print(db.set_table(TABLE).exists(sno=""))
    # print(db.set_table(TABLE).exists({"key": "tQ0gK2eM4fR2uD1xK", "sno": "3123358142", "role": "All"}))
    # print(db.set_table(TABLE).exists({"key": "xE2tX7cN8iZ6xQ1uG", "sno": None}))
    # print(db.set_table(TABLE).exists({"key": "xE2tX7cN8iZ6xQ1uG", "sno": ""}))
    # print(db.set_table(TABLE).exists({"key1": "xE2tX7cN8iZ6xQ1uG", "sno": ""}))
    """ insert_row/insert_rows """
    # db.set_table(TABLE)
    # obj = {"key": "哈哈哈4441", "sno": "2222222222222222222", "role": 1}
    # obj2 = {"key": "哈哈哈4444", "sno": "333333333333333333333", "role": ""}
    # obj3 = {"key": "哈哈哈55", "sno": "444444444444444444' or 1=1", "role": None}
    # id = db.insert_row(obj2)
    # print(id)
    # obj_list = [obj, obj2, obj3]
    # res = db.insert_rows(obj_list)
    # print(res)
    # res = db.set_table(TABLE).insert_row(id=22, key="wangkang", sno="3123358142", role="All")
    # print(res)
    # res = db.insert_many(obj_list)
    # print(res)

    """ delete """
    # obj = {"key": "哈哈哈4441", "sno": "2", "role": 1}
    # obj2 = {"key": "哈哈哈4444", "sno": "2", "role": ""}
    # obj3 = {"key": "哈哈哈55", "sno": "3", "role": None}
    # obj_list = [obj, obj2, obj3]
    # print(db.set_table(TABLE).insert_many(obj_list))
    # print(db.delete_row(key="哈哈哈4444"))
    # print(db.delete_row(sno="2"))
    # print(db.delete_row({"key": "3", "sno": 2, "role": None}))
    # print(db.delete_row({"key": "3", "sno": 3, "role": 3}))
    # print(db.delete_row({"role": "1"}))
    # print(db.delete_rows(obj_list))
    # for i in range(10):
    #     print(db.insert_row({"key": i}))
    # db.delete_row(id=1)
    # db.delete_rows([{"id": 2}, {"id": 3}])
    # data = []
    # for i in range(0, 30):
    #     data.append({"key": str(i), "sno": str(i), "role": str(i)})
    # print(db.insert_rows(data))
    # print(db.delete_many(data))

    # db.set_table(TABLE)
    # print(db.select_all())
    # print(db.select(sno=2))
    # print(db.select(sno=None))
    # print(db.select(role=None))
    # print(db.select({"sno": "2", "role": "123"}))
    # print(db.select({"sno": "2", "role": 123}))
    # print(db.select({"key": "哈哈哈551"}))

    # obj = {"sno": "12"}
    # obj2 = {"key": "哈哈哈7777", "sno": "112", "role": "1"}
    # print(db.update(obj, obj2))

    # 测试create_table
    data1 = {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "label": "TEXT",
        "_id": "TEXT",
        "creator": "TEXT",
        "updater": "TEXT",
        "createTime": "TEXT",
        "updateTime": "TEXT",
        "userAgent": "TEXT",
        "flowDecision": "TEXT",
        "_widget_1616673287156": "TEXT",
        "_widget_1679462572706": "TEXT",
        "_widget_1617678690020": "TEXT",
        "_widget_1615827614721": "TEXT",
        "_widget_1615835360787": "TEXT",
        "_widget_1615835360820": "TEXT",
        "_widget_1615868277748": "TEXT",
        "_widget_1679382295430": "TEXT",
        "_widget_1680158790676": "TEXT",
        "_widget_1615827613948": "TEXT",
        "_widget_1615827614024": "TEXT",
        "_widget_1616127228841": "TEXT",
        "_widget_1646551883542": "TEXT",
        "_widget_1615827614179": "TEXT",
        "_widget_1615828535162": "TEXT",
        "_widget_1615827614346": "text",
        "_widget_1615853253200": "TEXT",
        "_widget_1646552160980": "TEXT",
        "_widget_1615827614230": "TEXT",
        "_widget_1650676573176": "TEXT",
        "_widget_1616138014817": "TEXT",
        "_widget_1679319585604": "TEXT",
        "_widget_1645530113180": "TEXT",
        "_widget_1615827614500": "TEXT",
        "_widget_1615827614519": "TEXT",
        "_widget_1615827614556": "TEXT",
        "_widget_1679206290832": "TEXT",
        "_widget_1679206291318": "TEXT",
        "_widget_1646573100387": "TEXT",
        "_widget_1646573100578": "TEXT",
        "_widget_1616161492340": "TEXT",
        "_widget_1646573100763": "TEXT",
        "_widget_1646573103096": "TEXT",
        "_widget_1615827614467": "TEXT",
        "_widget_1615868277437": "TEXT",
        "_widget_1679206291570": "TEXT",
        "_widget_1679206291997": "TEXT",
        "_widget_1679206292059": "TEXT",
        "_widget_1615827614316": "TEXT",
        "_widget_1615872450096": "TEXT",
        "_widget_1615827614331": "TEXT",
        "_widget_1615872450115": "TEXT",
        "_widget_1646573101933": "TEXT",
        "_widget_1646573101968": "TEXT",
        "_widget_1679206292413": "TEXT",
        "_widget_1679206292466": "TEXT",
        "_widget_1646573101063": "TEXT",
        "_widget_1617845711912": "TEXT",
        "_widget_1616138013810": "TEXT",
        "_widget_1710314345323": "TEXT",
        "_widget_1710314345885": "TEXT",
        "_widget_1710327754686": "TEXT",
        "_widget_1710329993986": "TEXT",
        "chargers_name": "TEXT",
        "appId": "TEXT",
        "entryId": "TEXT",
    }

    data2 = {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "key": "TEXT",
        "sno": "TEXT",
        "role": "TEXT",
    }
    # db.set_table("test").create_table(data1, True)
    # db.set_table("test").insert_row({"key": "123", "sno": "456", "role": "789"})
    # db.set_table("test").delete_table()
