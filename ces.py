#!/usr/bin/python3
import pymysql


class mysql_method(object):
    """
        mysql_method类实现对数据库的增删改查。
        为减少服务器数据库的负荷，数据库连接和断开单独封装好了私有函数，在增删改查的对外开发函数的定义中分别在开头和结尾建立和断开数据库连接

        Attributes:
            self.form_name ：用来存放数据库的名称
            self._db       :用来存放数据库连接，可以在创建和断开连接函数直接起传递作用

        Methods:
            add(self,user_id,add_line_name,add_data): 数据库增或改。
            search(self,user_id,line_name): 数据库内容查找。

        Usage:
            obj = mysql_method()
            obj.add(ID,列名（元组）,列数据（元组）)
            obj.方法2(ID,列名（元组）)
            ...
        """

    # 初始化
    def __init__(self):
        self.form_name = "test0322"
        self._db = pymysql.connect(host='rm-cn-x0r3nruad001532o.rwlb.rds.aliyuncs.com',
                                   user='Liao',
                                   port=3306,
                                   password='Liao123456',
                                   database='datatest0319')
        self._db.close()

    # 创建数据库连接
    def _db_connect(self):
        try:
            self._db = pymysql.connect(host='rm-cn-x0r3nruad001532o.rwlb.rds.aliyuncs.com',
                                       user='Liao',
                                       port=3306,
                                       password='Liao123456',
                                       database='datatest0319')
        except pymysql.MySQLError as e:
            print(f"Failed to connect to the database: {e}")
            return None

    # 断开数据库连接
    def _db_destroy(self):
        self._db.close()

    # 增/改
    def add(self, user_id, add_line_name, add_data):
        self._db_connect()
        # cursor = self._db.cursor()  # 创建一个游标对象
        # insert_statement = "INSERT INTO test0322 (User_id, Other_column1, Other_column2, ...) VALUES (%s, %s, %s, ...)"
        # cursor.execute(insert_statement)  # 用execute方法执行SQL添加
        print("00")
        try:
            cursor = self._db.cursor()  # 创建一个游标对象
            # 确保add_line_name和add_data的长度相同，并且对应
            if len(add_line_name) != len(add_data):
                raise ValueError("列名和数据长度不匹配")

            # 检查当前ID是否已存在
            sql_check = f"SELECT * FROM {self.form_name} WHERE User_id = \"{user_id}\""
            cursor.execute(sql_check)
            result = cursor.fetchall()
            # print("11select:",sql_check,result)
            if result:
                # ID已经存在，更新其他列

                update_statement = f"UPDATE {self.form_name} SET " + ", ".join(
                    [f"{col} = \"%s\" " for col in add_line_name]) % (add_data) + f" WHERE User_id = \"{user_id}\""
                # print(update_query)
                cursor.execute(update_statement)
                self._db.commit()  # 提交修改，修改之后必须调用这个函数才能把修改内容提交到云端数据库
                # self._db.commit()
                print("添加成功： ")
            else:
                insert_statement = f"INSERT INTO {self.form_name} (User_id,{', '.join(add_line_name)}) VALUES (" + f"\"{user_id}\"," + " ,".join(
                    [f"\"{data}\"" for data in add_data]) + ")"
                print("insert:", insert_statement)
                cursor.execute(insert_statement)  # 使用execute方法执行SQL添加
                self._db.commit()  # 提交事务

        except Exception as e:
            print(f"An error occurred: {e}")
            # self._db.rollback()  # 发生错误时回滚
        finally:
            cursor.close()  # 关闭游标

        self._db_destroy()

    # 查  0是正常查询到数据，-1是没查到叫User_id的列，-2是没查到该用户id ,-3是列名不存在,
    # 返回值是查询ID的行数据
    def search(self, user_id, line_name=None):
        self._db_connect()
        fun_fallback = 0
        try:

            cursor = self._db.cursor()  # 创建一个游标对象
            if line_name:
                search = f"SELECT User_id,{','.join(line_name)}  FROM test0322 WHERE User_id = \"{user_id}\""
            else:
                search = f"SELECT * FROM \"{self.form_name}\" WHERE User_id = \"{user_id}\""
            # print(search)

            cursor.execute(search)  # 用execute方法执行SQL查询

            # 获取列名
            # column_names = [desc[0] for desc in cursor.description]
            # 打印列名
            # print("Column names:", column_names)

            # 获取查询结果
            user_data = cursor.fetchall()  # 即使查询结果为仅1行，返回的结果为(('1', None, None, None),) 这样的第二个元素为空的元组

            # print(user_data[0],' ',user_data)

            # 检查列是否存在
            if user_data:
                # 列存在，检查是否找到了数据
                result = user_data[0]  # 这个fetchone 会把队列的第一项取出来，后面再用fetchall就会少一行数据
                if result is None:
                    # print("没有找到对应的用户ID。")
                    fun_fallback = -2
                else:
                    # print("找到数据：",result)
                    fun_fallback = result
            else:
                # 没有找到User_id列
                # print("表中没有User_id列。")
                fun_fallback = -1

        except pymysql.err.OperationalError as e:
            # 捕获操作错误
            print(f"数据库操作错误： {e}")
            cursor.close()
            self._db_destroy()
            fun_fallback = -3
        finally:
            cursor.close()
            self._db_destroy()
            return fun_fallback


if __name__ == "__main__":
    sql = mysql_method()
    re = sql.search('5', ("Qmsg_key", "data_test"))
    print(re)
    # sql.add('8',("Qmsg_key","data_test"),("51","hello"))
    '''
    a = '1'
    id = ("id0","id1")
    data = ("data0","data1")
    str = f"123{a}"+", ".join([f"{id_i} = %s" for id_i in id])%(data)
    print(str)
    print(", ".join([f"{id_i} = %s" for id_i in id]))

    user_id = "8"
    add_line_name = ("Qmsg_key","data_test")
    add_data = ("1","hello")
    insert_statement = f"INSERT INTO test0322 (User_id,{', '.join(add_line_name)}) VALUES ("+f"\"{user_id}\","+" ,".join([f"\"{data}\"" for data in add_data])+")"
    print(insert_statement)

    user_id = "8"
    Line = ("Qmsg_key","data_test")
    Line = "*"
    search = f"SELECT User_id,{','.join(Line) }  FROM test0322 WHERE User_id = \"{user_id}\""
    print(search)
    '''

