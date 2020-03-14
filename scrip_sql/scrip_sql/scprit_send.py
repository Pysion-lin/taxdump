from utils.sql_client import BaseTaxdump
import pandas as pd
from sqlalchemy import text
import pymysql


class BaseUpdateToMysql(BaseTaxdump):
    def __init__(self,path,database,tabname):
        super().__init__(database)
        # path = 'E:/work/taxdump/nodes.dmp'
        self.nodes = pd.read_csv(path, sep='\t|\t', header=None,iterator=True)
        self.tabname = tabname
        self.database = database

    # 解析数据
    def parse_data(self,data):
        '''
        :param data: data为tuple
        :return:
        '''
        list_data = []
        for index, row in data.iterrows():
            df = row[0::2]
            df = df.values.tolist()
            tuple_data = (df[0],df[1],df[2],df[3],df[4],df[5],df[6],df[7],df[8],df[9],df[10],df[11],df[12])
            # list_data.append(tuple_data)
            self.send_data(tuple_data)
        # return list_data

    # 向数据库写入数据
    def send_data(self,data):
        if data:
            # 创建数据库连接
            # taxdum = BaseTaxdump(self.database)
            # for data in datas:
                # print(data)
            try:
                re = self.insert_data(data,self.tabname)
                if re==0:
                    # print('数据入库ok')
                    return True
                else:
                    # print('数据入库ng')
                    return False
            except Exception as e:
                print(e)
                print(data)
            #     print('校验出错')

    # 启动数据更新
    def run(self,chunkSize,size):
        '''
        :param chunkSize: 2
        :param size: 20
        :return:
        '''
        reader = self.nodes
        loop = 0
        chunks = []
        while loop < size:
            try:
                chunk = reader.get_chunk(chunkSize)
                chunks.append(chunk)
                loop += chunkSize
                self.parse_data(chunk)
            except Exception as e:
                #         loop = False
                size = 0
                print(e)
                # print("Iteration is stopped")


class CitationUpdate(BaseUpdateToMysql):
    def parse_data(self,data):
        '''
        :param data: data为tuple
        :return:
        '''
        for index, row in data.iterrows():
            df = row[0::2]
            df = df.values.tolist()
            if str(df[1]) == 'nan':
                df[1] = r'0'
            if str(df[4]) == 'nan':
                df[4] = r'0'
            if str(df[5]) == 'nan':
                df[5] = r'0'
            if str(df[6]) == 'nan':
                df[6] = r'0'
            tuple_data = (df[0],df[1],df[2],df[3],df[4],df[5],df[6])
            self.send_data(tuple_data)

    def get_sql_comment(self, data_tuple, table_name):
        self.sql_comment = r"insert into %s values %s;" % (table_name, data_tuple)
        # self.sql_comment = pymysql.escape_string(self.sql_comment)
        self.sql_comment = self.sql_comment.replace(':',"\:")
        # print(self.sql_comment)

        return text(self.sql_comment)

class MergedUpdate(BaseUpdateToMysql):
    def parse_data(self,data):
        '''
        :param data: data为tuple
        :return:
        '''
        for index, row in data.iterrows():
            df = row[0::2]
            df = df.values.tolist()
            tuple_data = (df[0],df[1])
            self.send_data(tuple_data)

    def get_sql_comment(self, data_tuple, table_name):
        self.sql_comment = r"insert into %s(old_tax_id,new_tax_id) values %s;" % (table_name, data_tuple)
        self.sql_comment = self.sql_comment.replace(':', "/:")
        return text(self.sql_comment)

if __name__ == '__main__':
    # citations = CitationUpdate('E:/work/scrip_sql/citations.dmp','taxdump2','taxdump_citations')
    citations = CitationUpdate('E:/work/taxdump/citations.dmp', 'taxdump2', 'taxdump_citations')
    citations.run(1,54469)
    # citations.run(1, 1)
    # citations = MergedUpdate('E:/work/taxdump/merged.dmp', 'taxdump2', 'taxdump_merged')
    #
    # citations.run(1, 56875)
