from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy import text
import pymysql


class BaseTaxdump(object):
	__instance = None

	def __init__(self,database):
		self.client = "mysql+pymysql://root:123456@127.0.0.1:3306/{}?charset=utf8".format(database)
		self.engine = create_engine(
		self.client,
		max_overflow=0,  # 超过连接池大小外最多创建的连接
		pool_size=5,  # 连接池大小
		pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
		pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）
		)

		self.SessionFactory = sessionmaker(bind=self.engine)
		self.session = scoped_session(self.SessionFactory)

	def __new__(cls, *args, **kwargs):
		if not cls.__instance:
			cls.__instance = super(BaseTaxdump, cls).__new__(cls)
		return cls.__instance

	# 向数据库提交数据
	def insert_data(self,data_tuple,table_name):
		'''

		:param data_tuple: 插入的数据
		:param table_name: 插入的数据表
		:return:
		'''
		# sql_comment = r"insert into %s" % table_name + " values " + str(data_tuple) + ";"
		# self.sql_comment = r"insert into %s values %s;" % (table_name,data_tuple)
		# print(sql_comment)
		try:
			sql_comment = self.get_sql_comment(data_tuple, table_name)
			# print('prix:',sql_comment)
			cursor = self.session.execute(sql_comment)
			self.session.commit()
			result = cursor.lastrowid
			# print(cursor.lastrowid)
			return result
		except Exception as e:
			print(e)

	# 提供获取sql语句的方法，方便重写
	def get_sql_comment(self,data_tuple,table_name):
		self.sql_comment = r"insert into %s values %s;" % (table_name, data_tuple)
		return self.sql_comment

	# 查询数据库数据
	def select_data(self,sql_comment):
		cursor = self.session.execute(sql_comment)
		result = cursor.fetchall()
		return result

	def __del__(self):
		self.session.remove()


if __name__ == '__main__':
	taxdump = BaseTaxdump('taxdump2')

	# 单例
	# taxdump2 = BaseTaxdump('taxdump2')
	# print(taxdump,taxdump2)

	# 写入模式
	# data = (6, 'The domestic cat: perspective on the nature and diversity of cats.', 0, 8603894, '', 'nan', '9685')
	# print(taxdump.insert_data(data,'taxdump_citations'))

	# 读取模式
	# sql = r'select * from taxdump_merged limit 10'
	# print(taxdump.select_data(sql))

