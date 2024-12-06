columns = ["id", "name"]
values = [[1, "wangkang"], [2, "wangkang"]]

# 方法一
print()


def tuple2json(column_names, data) -> dict:
    tmp_ = {}
    for idx, value in enumerate(data):
        tmp_[column_names[idx]] = value
    return tmp_


# 方法二
print(tuple2json(columns, values))
