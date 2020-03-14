from django.shortcuts import render

# Create your views here.


import pandas as pd
import pymysql
import pandas as pd
from sqlalchemy import create_engine
from .models import Nodes
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import NodeModelSerializer,MergedModelSerializer,CitationsModelSerializer,GencodeModelSerializer,DelNodeModelSerializer,DivisionSerializer,NameModelSerializer
from .models import Nodes,Merged,Gencode,Name,DelNode,Citations,Division
from rest_framework import status


class NodeDumpList(APIView):
    def get(self,request):
        Nodes_list_obj = Nodes.objects.first()
        # get方法时,自定义序列化参数是查询的到的表的model对象,many
        if Nodes_list_obj:
            msg = NodeModelSerializer(Nodes_list_obj,many=False)
        else:
            return Response(data={'msg':'None'})
        return Response(data=msg.data)
    def post(self,request):
        # post,put方法时,这个自定义序列里面的参数是data=request.data,many
        msg = NodeModelSerializer(data=request.data, many=False)
        if msg.is_valid():
            msg.save()  # create
            return Response(msg.data)
        else:
            return Response(msg.errors)
class NodeDumpDetial(APIView):
    def get(self,request,pk):
        try:
            Nodes_list_obj = Nodes.objects.get(pk=pk)
        except Nodes.DoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)
        # get方法时,自定义序列化参数是查询的到的表的model对象,many
        if Nodes_list_obj:
            msg = NodeModelSerializer(Nodes_list_obj, many=False)
        else:
            return Response(data={'msg': 'None'})
        return Response(data=msg.data)

class GencodeDetial(APIView):
    def get(self,request,pk):
        try:
            Gencode_list_obj = Gencode.objects.get(pk=pk)
        except Gencode.DoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)
        # get方法时,自定义序列化参数是查询的到的表的model对象,many
        if Gencode_list_obj:
            msg = GencodeModelSerializer(Gencode_list_obj, many=False)
        else:
            return Response(data={'msg': 'None'})
        return Response(data=msg.data)

class NameDetial(APIView):
    def get(self,request,pk):
        try:
            Name_list_obj = Name.objects.get(pk=pk)
        except Name.DoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)
        # get方法时,自定义序列化参数是查询的到的表的model对象,many
        if Name_list_obj:
            msg = NameModelSerializer(Name_list_obj, many=False)
        else:
            return Response(data={'msg': 'None'})
        return Response(data=msg.data)

class CitationsDetial(APIView):
    def get(self,request,pk):
        try:
            Citations_list_obj = Citations.objects.get(pk=pk)
        except Citations.DoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)
        # get方法时,自定义序列化参数是查询的到的表的model对象,many
        if Citations_list_obj:
            msg = CitationsModelSerializer(Citations_list_obj, many=False)
        else:
            return Response(data={'msg': 'None'})
        return Response(data=msg.data)

class DivisionDetial(APIView):
    def get(self,request,pk):
        try:
            Division_list_obj = Division.objects.get(pk=pk)
        except Division.DoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)
        # get方法时,自定义序列化参数是查询的到的表的model对象,many
        if Division_list_obj:
            msg = DivisionSerializer(Division_list_obj, many=False)
        else:
            return Response(data={'msg': 'None'})
        return Response(data=msg.data)

# 读取dump文件
# nodes = pd.read_csv('E:/work/taxdump/nodes.dmp',sep='\t|\t',header=None)
# 提取dump文件内容
# rd = nodes.head()
# for index,row in rd.iterrows():
#     df = row[0::2]
#     print(df.values.tolist())


class BaseUpdateToMysql(object):
    def __init__(self,path , modelserializer):
        # path = 'E:/work/taxdump/nodes.dmp'
        self.nodes = pd.read_csv(path, sep='\t|\t', header=None,iterator=True)
        self.ModelSerializer = modelserializer
    # 解析数据
    def parse_data(self,data):
        '''
        :param data: data为dataframe
        :return:
        '''
        list_data = []
        for index, row in data.iterrows():
            df = row[0::2]
            df = df.values.tolist()
            dict_data = {
                "tax_id": df[0],
                "parent_tax_id": df[1],
                "rank": df[2],
                "embl_code": df[3],
                "division_id": df[4],
                "inherited_div_flag": df[5],
                "genetic_code_id_id": df[6],
                "genetic_code_id": df[6],
                "inherited_GC_flag": df[7],
                "mitochondrial_genetic_code_id": df[8],
                "inherited_MGC_flag": df[9],
                "GenBank_hidden_flag": df[10],
                "hidden_subtree_root_flag": df[11],
                "comments": df[12],
            }
            list_data.append(dict_data)
        return list_data
    # 向数据库写入数据
    def send_data(self,datas):
        if datas:
            for data in datas:
                # print(data)
                try:
                    msg = self.ModelSerializer(data=data, many=False)
                    if msg.is_valid(raise_exception=True):
                        msg.save()  # create
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


class NodeUpdate(BaseUpdateToMysql):
    pass

class DivisionUpdata(BaseUpdateToMysql):
    def parse_data(self,data):
        list_data = []
        for index, row in data.iterrows():
            df = row[0::2]
            df = df.values.tolist()
            dict_data = {
                "division_id": df[0],
                "division_code": df[1],
                "division_name": df[2],
                "comments": df[3],
            }
            list_data.append(dict_data)
        return list_data

class GencodeUpdata(BaseUpdateToMysql):
    def parse_data(self,data):
        list_data = []
        for index, row in data.iterrows():
            df = row[0::2]
            df = df.values.tolist()
            dict_data = {
                "genetic_code_id": df[0],
                "abbreviation": df[1],
                "name": df[2],
                "code": df[3],
                "starts": df[4],
            }
            list_data.append(dict_data)
        return list_data

class NameUpdata(BaseUpdateToMysql):
    def parse_data(self,data):
        list_data = []
        for index, row in data.iterrows():
            df = row[0::2]
            df = df.values.tolist()
            dict_data = {
                "tax_id": df[0],
                "name_txt": df[1],
                "unique_name": df[2],
                "name_class": df[3],
            }
            list_data.append(dict_data)
        return list_data

class DelNodeUpdata(BaseUpdateToMysql):
    def parse_data(self,data):
        list_data = []
        for index, row in data.iterrows():
            df = row[0::2]
            df = df.values.tolist()
            dict_data = {
                "tax_id": df[0],

            }
            list_data.append(dict_data)
        return list_data

class MergedUpdata(BaseUpdateToMysql):
    def parse_data(self,data):
        list_data = []
        for index, row in data.iterrows():
            df = row[0::2]
            df = df.values.tolist()
            dict_data = {
                "old_tax_id": df[0],
                "new_tax_id": df[1],

            }
            list_data.append(dict_data)
        return list_data

class CitationsUpdata(BaseUpdateToMysql):
    def parse_data(self,data):
        list_data = []
        for index, row in data.iterrows():
            df = row[0::2]
            df = df.values.tolist()
            dict_data = {
                "cit_id": df[0],
                "cit_key": df[1],
                "pubmed_id": df[2],
                "medline_id": df[3],
                "url": df[4],
                "text": df[5],
                "taxid_list": df[6],
            }
            list_data.append(dict_data)
            return list_data


# di = MergedUpdata('E:/work/taxdump/merged.dmp',MergedModelSerializer)
# di.run(1,56876)
#
# di = CitationsUpdata('E:/work/taxdump/citations.dmp',CitationsModelSerializer)
# di.run(1,54469)

# di = DelNodeUpdata('E:/work/taxdump/delnodes.dmp',DelNodeModelSerializer)
# di.run(2,427291)

# di = GencodeUpdata('E:/work/taxdump/gencode.dmp',GencodeModelSerializer)
# di.run(1,30)


# di = DivisionUpdata('E:/work/taxdump/division.dmp',DivisionSerializer)
# di.run(1,30)



# di = NodeUpdate('E:/work/taxdump/nodes.dmp',NodeModelSerializer)
# di.run(1,2230839)


# di = NameUpdata('E:/work/taxdump/nodes.dmp',NameModelSerializer)
# di.run(1,3163914)