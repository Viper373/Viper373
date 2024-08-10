import pymysql

# 连接到 MySQL 数据库
cnx = pymysql.connect(
    host="62.234.5.84",
    user="viper3",
    password="viper3",
    database="viper3"
)

# 创建游标对象
cursor = cnx.cursor()

# 执行查询获取每篇文章的字数
query = "SELECT LENGTH(post_content) FROM wp_posts WHERE (post_status = 'publish' or post_status = 'draft') and post_type = 'post' or post_type = 'page' or post_type = 'shuoshuo'"
cursor.execute(query)

# 获取查询结果
word_counts = [row[0] for row in cursor.fetchall()]

# 关闭游标
cursor.close()

# 计算总字数并打印结果
total_word_count = sum(word_counts)
print("🍎全站字数:", "{}k".format(total_word_count / 1000))