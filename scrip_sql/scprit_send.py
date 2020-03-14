from .sql_client import BaseTaxdump




class BaseUpdateToMysql(object):
    def __init__(self,path,database,tabname):
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
            list_data.append(dict_data)
        return list_data
    # 向数据库写入数据
    def send_data(self,datas):
        if datas:
            for data in datas:
                # print(data)
                try:
                   # 创建数据库连接
                    taxdum = BaseTaxdump(self.database)
                    re = taxdum.insert_data(data,self.tabname)
                    if re==0:
                        return True
                    else:
                        return False
                except Exception as e:
                    pass
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
                list_data = self.parse_data(chunk)
                self.send_data(list_data)
            except StopIteration:
                #         loop = False
                size = 0
                print("Iteration is stopped")
				
class CitationUpdate(BaseUpdateToMysql):
    def parse_data(self,data):
        '''
        :param data: data为tuple
        :return:
        '''
        list_data = []
        for index, row in data.iterrows():
            df = row[0::2]
            df = df.values.tolist()
            tuple_data = (df[0],df[1],df[2],df[3],df[4],df[5],df[6])
            list_data.append(tuple_data)
        return list_data
				
if __name__ == '__main__':
    citations = CitationUpdate('E:/work/taxdump/citations.dmp','taxdump2','taxdump_citations')
    citations.run(1,10)

