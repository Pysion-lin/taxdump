from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session


class BaseTaxdump(object):
	def __init__(self,database):
		self.engine = create_engine(
        "mysql+pymysql://root:123456@127.0.0.1:3306/{}?charset=utf8",
        max_overflow=0,  # 超过连接池大小外最多创建的连接
        pool_size=5,  # 连接池大小
        pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
        pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）
    ).format(database)
		
		self.SessionFactory = sessionmaker(bind=self.engine)
		self.session = scoped_session(self.SessionFactory)
	
	def insert_data(self,data_tuple,table_name):
	
		sql_comment = 'insert into  {}  values {};'.format(table_name,data_tuple)
		# print(sql_comment)
		cursor = self.session.execute(sql_comment)
		self.session.commit()
		result = cursor.lastrowid
		# print(cursor.lastrowid)
		return result
		
		
	def select_data(self,sql_comment):
		cursor = self.session.execute(sql_comment)
		result = cursor.fetchall()
		return result
		
	def __del__(self):
		self.session.remove()

if __name__ == '__main__':
	taxdump = BaseTaxdump('taxdump2')
	data = (6, 'The domestic cat: perspective on the nature and diversity of cats.', 0, 8603894, '', 'nan', '9685')
	print(taxdump.insert_data(data,'taxdump_citations'))