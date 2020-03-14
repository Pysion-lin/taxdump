from rest_framework import serializers
from .models import Nodes,Division,Gencode,Name,DelNode,Merged,Citations


class GencodeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gencode
        fields = '__all__'

class NodeModelSerializer(serializers.ModelSerializer):
    genetic_code_id = GencodeModelSerializer(read_only=True)
    class Meta:
        model = Nodes
        fields = '__all__'
class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = '__all__'


class NameModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Name
        fields = '__all__'

class DelNodeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DelNode
        fields = '__all__'

class MergedModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merged
        fields = '__all__'

class CitationsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Citations
        fields = '__all__'
