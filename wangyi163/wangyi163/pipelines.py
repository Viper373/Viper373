# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
import pymysql


class MySQLPipeline:
    def __init__(self):
        self.connect = pymysql.connect(host='localhost',
                                       user='root',
                                       passwd='ShadowZed666',
                                       charset='utf8',
                                       port=3306)
        self.cursor = self.connect.cursor()

    def open_spider(self, spider):
        print("开始保存数据")
        # 调用创建数据库和表的方法
        self._create_db_and_table()

    def close_spider(self, spider):
        print("数据保存完毕")
        self.connect.close()
        self.cursor.close()

    def process_item(self, item, spider):
        table_fields = item.get('table_fields')
        table_name = item.get('table_name')
        if table_fields is None or table_name is None:
            raise Exception('必须要传表名table_name和字段名table_fields，表名或者字段名不能为空')
        values_params = '%s, ' * (len(table_fields) - 1) + '%s'
        keys = ', '.join(table_fields)
        values = ['%s' % str(item.get(i, '')) for i in table_fields]
        self.connect.select_db('wangyi')
        insert_sql = 'insert into %s (%s) values (%s)' % (table_name, keys, values_params)
        try:
            self.cursor.execute(insert_sql, tuple(values))
            logging.info("数据插入成功 => " + '1')
        except Exception as e:
            logging.error("执行sql异常 => " + str(e))
            pass
        finally:
            # 要提交，不提交无法保存到数据库
            self.connect.commit()
        return item

    def _create_db_and_table(self):
        # 创建数据库
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS wangyi DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        self.connect.commit()  # 提交创建数据库的操作
        # 选择数据库
        self.connect.select_db('wangyi')
        # 创建表
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS job (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                productName VARCHAR(100),
                firstDepName VARCHAR(50),
                workPlaceName VARCHAR(20),
                postTypeFullName VARCHAR(255),
                description TEXT,
                requirement TEXT,
                recruitNum INT,
                reqEducationName VARCHAR(20) DEFAULT '学历不限',
                reqWorkYearsName VARCHAR(20) DEFAULT '经验不限',
                updateTime DATE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)
        self.connect.commit()  # 提交创建表的操作

    def _handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print(failure)